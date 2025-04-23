
#include "grid_logic.h"
#include <stdexcept> // For potential errors, though can_place returns bool

namespace trianglengin::cpp::grid_logic
{

  bool can_place(const GridData &grid_data, const ShapeCpp &shape, int r, int c)
  {
    if (shape.triangles.empty())
    {
      return false; // Cannot place an empty shape
    }

    for (const auto &tri_data : shape.triangles)
    {
      int dr, dc;
      bool shape_is_up;
      std::tie(dr, dc, shape_is_up) = tri_data;

      int target_r = r + dr;
      int target_c = c + dc;

      // 1. Check bounds
      if (!grid_data.is_valid(target_r, target_c))
      {
        return false;
      }

      // 2. Check death zone
      if (grid_data.is_death(target_r, target_c))
      {
        return false;
      }

      // 3. Check occupancy
      if (grid_data.is_occupied(target_r, target_c))
      {
        return false;
      }

      // 4. Check orientation match
      bool grid_is_up = grid_data.is_up(target_r, target_c);
      if (shape_is_up != grid_is_up)
      {
        return false;
      }
    }
    // If all checks passed for all triangles
    return true;
  }

  std::tuple<int, std::set<Coord>, LineFsSet> check_and_clear_lines(
      GridData &grid_data,
      const std::set<Coord> &newly_occupied_coords)
  {
    if (newly_occupied_coords.empty())
    {
      return {0, {}, {}};
    }

    const auto &coord_map = grid_data.get_coord_to_lines_map();
    LineFsSet candidate_lines;

    // 1. Find all maximal lines potentially affected by the new placements
    for (const auto &coord : newly_occupied_coords)
    {
      auto it = coord_map.find(coord);
      if (it != coord_map.end())
      {
        // Add all lines associated with this coordinate to the candidates
        candidate_lines.insert(it->second.begin(), it->second.end());
      }
    }

    LineFsSet lines_to_clear;
    std::set<Coord> coords_to_clear;

    // 2. Check each candidate line for completion
    for (const auto &line_fs : candidate_lines)
    {
      if (line_fs.size() < 2)
        continue; // Should not happen based on precomputation filter

      bool line_complete = true;
      for (const auto &coord : line_fs)
      {
        // A line is complete if ALL its coordinates are occupied
        if (!grid_data.is_occupied(std::get<0>(coord), std::get<1>(coord)))
        {
          line_complete = false;
          break;
        }
      }

      if (line_complete)
      {
        lines_to_clear.insert(line_fs);
        // Add coordinates from this completed line to the set to be cleared
        coords_to_clear.insert(line_fs.begin(), line_fs.end());
      }
    }

    // 3. Clear the identified coordinates
    if (!coords_to_clear.empty())
    {
      auto &occupied_grid = grid_data.get_occupied_grid_mut();
      auto &color_grid = grid_data.get_color_id_grid_mut();
      for (const auto &coord : coords_to_clear)
      {
        int r = std::get<0>(coord);
        int c = std::get<1>(coord);
        // Ensure we don't try to clear out-of-bounds (shouldn't happen)
        if (grid_data.is_valid(r, c))
        {
          occupied_grid[r][c] = false;
          color_grid[r][c] = NO_COLOR_ID;
        }
      }
    }

    return {static_cast<int>(lines_to_clear.size()), coords_to_clear, lines_to_clear};
  }

} // namespace trianglengin::cpp::grid_logic