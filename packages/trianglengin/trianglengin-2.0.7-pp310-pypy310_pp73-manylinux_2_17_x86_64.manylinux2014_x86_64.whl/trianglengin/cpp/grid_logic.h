// File: src/trianglengin/cpp/grid_logic.h
#ifndef TRIANGLENGIN_CPP_GRID_LOGIC_H
#define TRIANGLENGIN_CPP_GRID_LOGIC_H

#pragma once

#include <set>
#include <tuple>
#include <vector>

#include "grid_data.h" // Needs GridData definition
#include "structs.h"   // Needs ShapeCpp, Coord, LineFsSet definitions

namespace trianglengin::cpp
{

  // Forward declare GameStateCpp if needed by functions here
  class GameStateCpp;

  namespace grid_logic
  {
    bool can_place(const GridData &grid_data, const ShapeCpp &shape, int r, int c);

    std::tuple<int, std::set<Coord>, LineFsSet>
    check_and_clear_lines(GridData &grid_data, const std::set<Coord> &newly_occupied_coords);

  } // namespace grid_logic
} // namespace trianglengin::cpp

#endif // TRIANGLENGIN_CPP_GRID_LOGIC_H