// File: src/trianglengin/cpp/grid_data.cpp
#include "grid_data.h"
#include <stdexcept>
#include <set>
#include <algorithm>
#include <iostream>

namespace trianglengin::cpp
{

  // Constructor: Initialize config_ by copying the passed config
  GridData::GridData(const EnvConfigCpp &config)
      : config_(config), // Copy config here
        rows_(config_.rows),
        cols_(config_.cols)
  {
    if (rows_ <= 0 || cols_ <= 0)
    {
      throw std::invalid_argument("Grid dimensions must be positive.");
    }
    occupied_grid_.assign(rows_, std::vector<bool>(cols_, false));
    color_id_grid_.assign(rows_, std::vector<int8_t>(cols_, NO_COLOR_ID));
    death_grid_.assign(rows_, std::vector<bool>(cols_, true));

    if (config_.playable_range_per_row.size() != static_cast<size_t>(rows_))
    {
      throw std::invalid_argument("Playable range size mismatch with rows.");
    }
    for (int r = 0; r < rows_; ++r)
    {
      const auto &[start_col, end_col] = config_.playable_range_per_row[r];
      if (start_col < 0 || end_col > cols_ || start_col > end_col) // Allow start == end
      {
        throw std::invalid_argument("Invalid playable range for row " + std::to_string(r));
      }
      if (start_col < end_col)
      {
        for (int c = start_col; c < end_col; ++c)
        {
          death_grid_[r][c] = false;
        }
      }
    }
    precompute_lines();
  }

  // Copy constructor: Explicitly copy all members
  GridData::GridData(const GridData &other)
      : config_(other.config_), // Copy config value
        rows_(other.rows_),
        cols_(other.cols_),
        occupied_grid_(other.occupied_grid_),
        color_id_grid_(other.color_id_grid_),
        death_grid_(other.death_grid_),
        lines_(other.lines_),
        coord_to_lines_map_(other.coord_to_lines_map_)
  {
    // All members are copyable, default member-wise copy is sufficient here,
    // but being explicit ensures correctness if members change later.
  }

  // Copy assignment operator: Explicitly copy all members
  GridData &GridData::operator=(const GridData &other)
  {
    if (this != &other)
    {
      config_ = other.config_; // Copy config value
      rows_ = other.rows_;
      cols_ = other.cols_;
      occupied_grid_ = other.occupied_grid_;
      color_id_grid_ = other.color_id_grid_;
      death_grid_ = other.death_grid_;
      lines_ = other.lines_;
      coord_to_lines_map_ = other.coord_to_lines_map_;
    }
    return *this;
  }

  void GridData::reset()
  {
    for (int r = 0; r < rows_; ++r)
    {
      std::fill(occupied_grid_[r].begin(), occupied_grid_[r].end(), false);
      std::fill(color_id_grid_[r].begin(), color_id_grid_[r].end(), NO_COLOR_ID);
    }
  }

  bool GridData::is_valid(int r, int c) const
  {
    return r >= 0 && r < rows_ && c >= 0 && c < cols_;
  }

  bool GridData::is_death(int r, int c) const
  {
    if (!is_valid(r, c))
    {
      throw std::out_of_range("Coordinates (" + std::to_string(r) + "," + std::to_string(c) + ") out of bounds.");
    }
    return death_grid_[r][c];
  }

  bool GridData::is_occupied(int r, int c) const
  {
    if (!is_valid(r, c))
    {
      throw std::out_of_range("Coordinates (" + std::to_string(r) + "," + std::to_string(c) + ") out of bounds.");
    }
    // An occupied cell cannot be a death cell by game logic after placement/clearing
    return occupied_grid_[r][c];
  }

  std::optional<int> GridData::get_color_id(int r, int c) const
  {
    if (!is_valid(r, c) || death_grid_[r][c] || !occupied_grid_[r][c])
    {
      return std::nullopt;
    }
    return color_id_grid_[r][c];
  }

  bool GridData::is_up(int r, int c) const
  {
    return (r + c) % 2 != 0;
  }

  bool GridData::is_live(int r, int c) const
  {
    return is_valid(r, c) && !death_grid_[r][c];
  }

  std::optional<Coord> GridData::get_neighbor(int r, int c, const std::string &direction, bool backward) const
  {
    bool up = is_up(r, c);
    int nr = -1, nc = -1;

    if (direction == "h")
    {
      int dc = backward ? -1 : 1;
      nr = r;
      nc = c + dc;
    }
    else if (direction == "d1")
    { // TL-BR
      if (backward)
      {
        nr = up ? r : r - 1;
        nc = up ? c - 1 : c;
      }
      else
      {
        nr = up ? r + 1 : r;
        nc = up ? c : c + 1;
      }
    }
    else if (direction == "d2")
    { // BL-TR
      if (backward)
      {
        nr = up ? r + 1 : r;
        nc = up ? c : c - 1;
      }
      else
      {
        nr = up ? r : r - 1;
        nc = up ? c + 1 : c;
      }
    }
    else
    {
      throw std::invalid_argument("Unknown direction: " + direction);
    }

    if (!is_valid(nr, nc))
      return std::nullopt;
    return Coord{nr, nc};
  }

  void GridData::precompute_lines()
  {
    lines_.clear();
    coord_to_lines_map_.clear();
    std::set<Line> maximal_lines_set;
    std::set<std::tuple<Coord, std::string>> processed_starts;
    const std::vector<std::string> directions = {"h", "d1", "d2"};

    for (int r_init = 0; r_init < rows_; ++r_init)
    {
      for (int c_init = 0; c_init < cols_; ++c_init)
      {
        if (!is_live(r_init, c_init))
          continue;
        Coord start_coord = {r_init, c_init};
        for (const auto &direction : directions)
        {
          Coord line_start_coord = start_coord;
          // Find the true start of the line segment in this direction
          while (true)
          {
            auto prev_coord_opt = get_neighbor(std::get<0>(line_start_coord), std::get<1>(line_start_coord), direction, true);
            if (prev_coord_opt && is_live(std::get<0>(*prev_coord_opt), std::get<1>(*prev_coord_opt)))
            {
              line_start_coord = *prev_coord_opt;
            }
            else
              break;
          }
          // Check if we already processed this line starting from this coordinate and direction
          if (processed_starts.count({line_start_coord, direction}))
            continue;

          // Trace the line forward from the true start
          Line current_line;
          std::optional<Coord> trace_coord_opt = line_start_coord;
          while (trace_coord_opt && is_live(std::get<0>(*trace_coord_opt), std::get<1>(*trace_coord_opt)))
          {
            current_line.push_back(*trace_coord_opt);
            trace_coord_opt = get_neighbor(std::get<0>(*trace_coord_opt), std::get<1>(*trace_coord_opt), direction, false);
          }

          // Store the line if it's long enough and mark it as processed
          if (current_line.size() >= 2) // Only store lines of length 2 or more
          {
            maximal_lines_set.insert(current_line);
            processed_starts.insert({line_start_coord, direction});
          }
        }
      }
    }

    // Convert set to vector and sort for deterministic order
    lines_ = std::vector<Line>(maximal_lines_set.begin(), maximal_lines_set.end());
    std::sort(lines_.begin(), lines_.end(), [](const Line &a, const Line &b)
              {
            if (a.empty() || b.empty()) return b.empty(); // Handle empty lines if they somehow occur
            // Sort primarily by starting row, then starting column, then size
            if (std::get<0>(a[0]) != std::get<0>(b[0])) return std::get<0>(a[0]) < std::get<0>(b[0]);
            if (std::get<1>(a[0]) != std::get<1>(b[0])) return std::get<1>(a[0]) < std::get<1>(b[0]);
            return a.size() < b.size(); });

    // Build the coordinate-to-lines map
    for (const auto &line_vec : lines_)
    {
      // Use a set of Coords (LineFs) as the value in the map for efficient lookup
      LineFs line_fs(line_vec.begin(), line_vec.end());
      for (const auto &coord : line_vec)
      {
        coord_to_lines_map_[coord].insert(line_fs);
      }
    }
  }

} // namespace trianglengin::cpp