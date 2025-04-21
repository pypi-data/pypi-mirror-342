// File: src/trianglengin/cpp/game_state.h
#ifndef TRIANGLENGIN_CPP_GAME_STATE_H
#define TRIANGLENGIN_CPP_GAME_STATE_H

#pragma once

#include <vector>
#include <set>
#include <optional>
#include <random>
#include <memory>
#include <string> // Include string for optional<string>
#include <tuple>  // Include tuple for std::tuple

#include "config.h"
#include "structs.h"
#include "grid_data.h"
// Remove direct includes causing cycles if possible, use forward declarations
// #include "grid_logic.h" // Included by game_state.cpp
// #include "shape_logic.h" // Included by game_state.cpp

namespace trianglengin::cpp
{

  class GameStateCpp
  {
  public:
    explicit GameStateCpp(const EnvConfigCpp &config, unsigned int initial_seed);

    // --- Rule of 5 ---
    ~GameStateCpp() = default;                                        // Default destructor
    GameStateCpp(const GameStateCpp &other);                          // Copy constructor
    GameStateCpp &operator=(const GameStateCpp &other);               // Copy assignment operator
    GameStateCpp(GameStateCpp &&other) noexcept = default;            // Default move constructor
    GameStateCpp &operator=(GameStateCpp &&other) noexcept = default; // Default move assignment operator

    void reset();
    std::tuple<double, bool> step(Action action);
    bool is_over() const;
    double get_score() const;
    const std::set<Action> &get_valid_actions(bool force_recalculate = false);
    int get_current_step() const;
    std::optional<std::string> get_game_over_reason() const;
    GameStateCpp copy() const; // Keep Python-facing copy method
    void debug_toggle_cell(int r, int c);
    void invalidate_action_cache(); // Moved to public
    // Debug method to force shapes into slots
    void debug_set_shapes(const std::vector<std::optional<ShapeCpp>> &new_shapes);

    // Accessors needed by logic functions or bindings
    const GridData &get_grid_data() const { return grid_data_; }
    GridData &get_grid_data_mut() { return grid_data_; }
    const std::vector<std::optional<ShapeCpp>> &get_shapes() const { return shapes_; }
    std::vector<std::optional<ShapeCpp>> &get_shapes_mut() { return shapes_; }
    const EnvConfigCpp &get_config() const { return config_; }
    // Expose RNG state for copying if needed (or handle seeding in copy)
    std::mt19937 get_rng_state() const { return rng_; }

  private:
    EnvConfigCpp config_;
    GridData grid_data_;
    std::vector<std::optional<ShapeCpp>> shapes_;
    double score_;
    int current_step_;
    bool game_over_;
    std::optional<std::string> game_over_reason_;
    mutable std::optional<std::set<Action>> valid_actions_cache_; // Mutable for const getter
    std::mt19937 rng_;

    void check_initial_state_game_over();
    void force_game_over(const std::string &reason);
    // void invalidate_action_cache(); // Moved from private
    void calculate_valid_actions_internal() const; // Made const

    // Action encoding/decoding (can be private if only used internally)
    Action encode_action(int shape_idx, int r, int c) const;
    std::tuple<int, int, int> decode_action(Action action) const;
  };

} // namespace trianglengin::cpp

#endif // TRIANGLENGIN_CPP_GAME_STATE_H