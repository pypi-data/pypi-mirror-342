// File: src/trianglengin/cpp/grid_data.h
#ifndef TRIANGLENGIN_CPP_GRID_DATA_H
#define TRIANGLENGIN_CPP_GRID_DATA_H

#pragma once

#include <vector>
#include <set>
#include <map>
#include <tuple>
#include <memory>
#include <optional>
#include <string>
#include <stdexcept>

#include "config.h"
#include "structs.h"

namespace trianglengin::cpp
{
  using Line = std::vector<Coord>;
  using LineFs = std::set<Coord>;
  using LineFsSet = std::set<LineFs>;
  using CoordMap = std::map<Coord, LineFsSet>;

  class GridData
  {
  public:
    // Constructor takes config by const reference but stores by value
    explicit GridData(const EnvConfigCpp &config);

    void reset();
    bool is_valid(int r, int c) const;
    bool is_death(int r, int c) const;
    bool is_occupied(int r, int c) const;
    std::optional<int> get_color_id(int r, int c) const;
    bool is_up(int r, int c) const;

    const std::vector<std::vector<bool>> &get_occupied_grid() const { return occupied_grid_; }
    const std::vector<std::vector<int8_t>> &get_color_id_grid() const { return color_id_grid_; }
    const std::vector<std::vector<bool>> &get_death_grid() const { return death_grid_; }
    std::vector<std::vector<bool>> &get_occupied_grid_mut() { return occupied_grid_; }
    std::vector<std::vector<int8_t>> &get_color_id_grid_mut() { return color_id_grid_; }

    const std::vector<Line> &get_lines() const { return lines_; }
    const CoordMap &get_coord_to_lines_map() const { return coord_to_lines_map_; }

    int rows() const { return rows_; }
    int cols() const { return cols_; }

    // Copy constructor
    GridData(const GridData &other);
    // Copy assignment operator
    GridData &operator=(const GridData &other);

    // Default move constructor/assignment should work now
    GridData(GridData &&other) noexcept = default;
    GridData &operator=(GridData &&other) noexcept = default;

  private:
    EnvConfigCpp config_; // Store config by value now
    int rows_;
    int cols_;
    std::vector<std::vector<bool>> occupied_grid_;
    std::vector<std::vector<int8_t>> color_id_grid_;
    std::vector<std::vector<bool>> death_grid_;

    std::vector<Line> lines_;
    CoordMap coord_to_lines_map_;

    void precompute_lines();
    bool is_live(int r, int c) const;
    std::optional<Coord> get_neighbor(int r, int c, const std::string &direction, bool backward) const;
  };

} // namespace trianglengin::cpp

#endif // TRIANGLENGIN_CPP_GRID_DATA_H
