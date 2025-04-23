// File: src/trianglengin/cpp/structs.h
#ifndef TRIANGLENGIN_CPP_STRUCTS_H
#define TRIANGLENGIN_CPP_STRUCTS_H

#pragma once

#include <vector>
#include <tuple>
#include <string>
#include <cstdint>
#include <utility>  // For std::move
#include <optional> // For optional members
#include <set>      // For previous valid actions

namespace trianglengin::cpp
{
  using Action = int;
  using Coord = std::tuple<int, int>;
  using ColorCpp = std::tuple<int, int, int>;
  using TriangleData = std::tuple<int, int, bool>;

  const int NO_COLOR_ID = -1;
  const int DEBUG_COLOR_ID = -2;

  struct ShapeCpp
  {
    std::vector<TriangleData> triangles;
    ColorCpp color;
    int color_id;

    ShapeCpp() : color_id(NO_COLOR_ID) {}
    ShapeCpp(std::vector<TriangleData> tris, ColorCpp c, int id)
        : triangles(std::move(tris)), color(c), color_id(id) {}

    bool operator==(const ShapeCpp &other) const
    {
      return triangles == other.triangles && color == other.color && color_id == other.color_id;
    }
  };

  // --- NEW: Structure to hold undo information ---
  struct StepUndoInfo
  {
    // Cells changed by placement or clearing
    // Stores (row, col, previous_occupied_state, previous_color_id)
    std::vector<std::tuple<int, int, bool, int8_t>> changed_cells;

    // Info about the shape that was consumed by the step
    int consumed_shape_slot = -1;
    std::optional<ShapeCpp> consumed_shape = std::nullopt;

    // Previous game state variables
    double previous_score = 0.0;
    int previous_step = 0;
    bool previous_game_over = false;
    std::optional<std::string> previous_game_over_reason = std::nullopt;

    // Cache invalidation marker (or potentially the previous cache itself)
    // Storing the previous cache might be large, maybe just invalidate?
    // Let's start by just marking that the cache *was* valid before the step.
    bool was_action_cache_valid = false;
    // OPTIONAL (more complex): Store the actual previous cache
    // std::optional<std::set<Action>> previous_valid_actions_cache = std::nullopt;
  };
  // --- END NEW ---

} // namespace trianglengin::cpp

#endif // TRIANGLENGIN_CPP_STRUCTS_H