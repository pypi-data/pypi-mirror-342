// File: src/trianglengin/cpp/game_state.cpp
#include "game_state.h"
#include "grid_logic.h"
#include "shape_logic.h"
#include <stdexcept>
#include <numeric>
#include <iostream>  // Keep iostream if other debug logs might be added later, or remove if not needed
#include <algorithm> // For std::min

namespace trianglengin::cpp
{

  GameStateCpp::GameStateCpp(const EnvConfigCpp &config, unsigned int initial_seed)
      : config_(config),
        grid_data_(config_), // Initialize GridData with config
        shapes_(config_.num_shape_slots),
        score_(0.0),
        current_step_(0),
        game_over_(false),
        rng_(initial_seed)
  {
    reset();
  }

  // --- Explicit Copy Constructor ---
  GameStateCpp::GameStateCpp(const GameStateCpp &other)
      : config_(other.config_),                           // Copy config
        grid_data_(other.grid_data_),                     // Use GridData's copy constructor
        shapes_(other.shapes_),                           // Copy vector of optional shapes
        score_(other.score_),                             // Copy score
        current_step_(other.current_step_),               // Copy step
        game_over_(other.game_over_),                     // Copy game over flag
        game_over_reason_(other.game_over_reason_),       // Copy reason
        valid_actions_cache_(other.valid_actions_cache_), // Copy the optional cache
        rng_(other.rng_)                                  // Copy the RNG state
  {
    // No additional logic needed if members handle their own copying well
  }

  // --- Explicit Copy Assignment Operator ---
  GameStateCpp &GameStateCpp::operator=(const GameStateCpp &other)
  {
    if (this != &other)
    {
      config_ = other.config_;
      grid_data_ = other.grid_data_; // Use GridData's copy assignment
      shapes_ = other.shapes_;
      score_ = other.score_;
      current_step_ = other.current_step_;
      game_over_ = other.game_over_;
      game_over_reason_ = other.game_over_reason_;
      valid_actions_cache_ = other.valid_actions_cache_; // Copy the optional cache
      rng_ = other.rng_;                                 // Copy the RNG state
    }
    return *this;
  }

  void GameStateCpp::reset()
  {
    grid_data_.reset();
    std::fill(shapes_.begin(), shapes_.end(), std::nullopt);
    score_ = 0.0;
    current_step_ = 0;
    game_over_ = false;
    game_over_reason_ = std::nullopt;
    valid_actions_cache_ = std::nullopt;
    shape_logic::refill_shape_slots(*this, rng_);
    check_initial_state_game_over();
  }

  void GameStateCpp::check_initial_state_game_over()
  {
    // Force calculation which updates the cache and potentially the game_over flag
    get_valid_actions(true);
    // No need to check cache emptiness here, get_valid_actions handles setting the flag
  }

  std::tuple<double, bool> GameStateCpp::step(Action action)
  {
    if (game_over_)
    {
      return {0.0, true};
    }

    // Ensure cache is populated before checking the action
    const auto &valid_actions = get_valid_actions(); // This populates cache if needed

    // Check against the (now guaranteed) populated cache
    if (valid_actions.find(action) == valid_actions.end())
    {
      // Invalid action detected
      force_game_over("Invalid action provided: " + std::to_string(action));
      score_ += config_.penalty_game_over; // Apply penalty
      return {config_.penalty_game_over, true};
    }

    int shape_idx, r, c;
    try
    {
      std::tie(shape_idx, r, c) = decode_action(action);
    }
    catch (const std::out_of_range &e)
    {
      force_game_over("Failed to decode action: " + std::to_string(action));
      score_ += config_.penalty_game_over;
      return {config_.penalty_game_over, true};
    }

    if (shape_idx < 0 || shape_idx >= static_cast<int>(shapes_.size()) || !shapes_[shape_idx].has_value())
    {
      force_game_over("Action references invalid/empty shape slot: " + std::to_string(shape_idx));
      score_ += config_.penalty_game_over;
      return {config_.penalty_game_over, true};
    }

    const ShapeCpp &shape_to_place = shapes_[shape_idx].value();

    // Re-check placement just before modification (defensive)
    if (!grid_logic::can_place(grid_data_, shape_to_place, r, c))
    {
      force_game_over("Placement check failed for valid action (logic error?). Action: " + std::to_string(action));
      score_ += config_.penalty_game_over;
      return {config_.penalty_game_over, true};
    }

    // --- Placement ---
    std::set<Coord> newly_occupied_coords;
    int placed_count = 0;
    auto &occupied_grid = grid_data_.get_occupied_grid_mut();
    auto &color_grid = grid_data_.get_color_id_grid_mut();
    for (const auto &tri_data : shape_to_place.triangles)
    {
      int dr, dc;
      bool is_up_ignored;
      std::tie(dr, dc, is_up_ignored) = tri_data;
      int target_r = r + dr;
      int target_c = c + dc;
      // Bounds check should be implicitly handled by can_place, but double-check
      if (!grid_data_.is_valid(target_r, target_c) || grid_data_.is_death(target_r, target_c))
      {
        force_game_over("Attempted placement out of bounds/death zone during execution. Action: " + std::to_string(action));
        score_ += config_.penalty_game_over;
        return {config_.penalty_game_over, true};
      }
      occupied_grid[target_r][target_c] = true;
      color_grid[target_r][target_c] = static_cast<int8_t>(shape_to_place.color_id);
      newly_occupied_coords.insert({target_r, target_c});
      placed_count++;
    }
    shapes_[shape_idx] = std::nullopt; // Clear the used shape slot

    // --- Line Clearing ---
    int lines_cleared_count;
    std::set<Coord> cleared_coords;
    LineFsSet cleared_lines_fs;
    std::tie(lines_cleared_count, cleared_coords, cleared_lines_fs) =
        grid_logic::check_and_clear_lines(grid_data_, newly_occupied_coords);
    int cleared_count = static_cast<int>(cleared_coords.size());

    // --- Refill ---
    bool all_slots_empty = true;
    for (const auto &shape_opt : shapes_)
    {
      if (shape_opt.has_value())
      {
        all_slots_empty = false;
        break;
      }
    }
    if (all_slots_empty)
    {
      shape_logic::refill_shape_slots(*this, rng_);
    }

    // --- Update State & Check Game Over ---
    current_step_++;
    invalidate_action_cache(); // Invalidate cache AFTER state changes
    get_valid_actions(true);   // Force recalculation AND update game_over_ flag if needed

    // --- Calculate Reward & Update Score ---
    double reward = 0.0;
    reward += static_cast<double>(placed_count) * config_.reward_per_placed_triangle;
    reward += static_cast<double>(cleared_count) * config_.reward_per_cleared_triangle;

    if (game_over_)
    {
      // Penalty was applied earlier if game over was due to invalid action this step.
      // If game over is due to lack of actions *after* this step, no penalty applies here.
    }
    else
    {
      reward += config_.reward_per_step_alive;
    }
    score_ += reward; // Update score based on calculated reward

    return {reward, game_over_}; // Return the potentially updated game_over_ flag
  }

  // --- Simplified is_over ---
  bool GameStateCpp::is_over() const
  {
    // The game_over_ flag is the single source of truth.
    // It's updated by step() [via get_valid_actions()] and reset().
    return game_over_;
  }

  void GameStateCpp::force_game_over(const std::string &reason)
  {
    if (!game_over_)
    {
      game_over_ = true;
      game_over_reason_ = reason;
      valid_actions_cache_ = std::set<Action>(); // Clear valid actions on game over
    }
  }

  double GameStateCpp::get_score() const
  {
    return score_;
  }

  const std::set<Action> &GameStateCpp::get_valid_actions(bool force_recalculate)
  {
    // If game is over, always return the cached empty set
    if (game_over_)
    {
      // Ensure cache is empty if game_over is true
      if (!valid_actions_cache_.has_value() || !valid_actions_cache_->empty())
      {
        valid_actions_cache_ = std::set<Action>();
      }
      return *valid_actions_cache_;
    }

    // If not forcing and cache exists, return it
    if (!force_recalculate && valid_actions_cache_.has_value())
    {
      return *valid_actions_cache_;
    }

    // Otherwise, calculate (which updates the mutable cache)
    calculate_valid_actions_internal();

    // Check if the calculation resulted in no valid actions, triggering game over
    if (!game_over_ && valid_actions_cache_->empty())
    {
      // Set the game over flag HERE, as this is the definitive check after calculation
      force_game_over("No valid actions available.");
    }

    // Return the calculated (and potentially now empty) cache
    return *valid_actions_cache_;
  }

  void GameStateCpp::invalidate_action_cache()
  {
    valid_actions_cache_ = std::nullopt;
  }

  // calculate_valid_actions_internal remains const, modifies mutable cache
  void GameStateCpp::calculate_valid_actions_internal() const
  {
    // This function should NOT set game_over_ directly.
    // It just calculates the set. The caller (get_valid_actions) checks if empty.
    std::set<Action> valid_actions;
    for (int shape_idx = 0; shape_idx < static_cast<int>(shapes_.size()); ++shape_idx)
    {
      if (!shapes_[shape_idx].has_value())
        continue;
      const ShapeCpp &shape = shapes_[shape_idx].value();
      for (int r = 0; r < config_.rows; ++r)
      {
        // Optimization: Check only within playable range? No, C++ can_place handles death zones.
        for (int c = 0; c < config_.cols; ++c)
        {
          if (grid_logic::can_place(grid_data_, shape, r, c))
          {
            valid_actions.insert(encode_action(shape_idx, r, c));
          }
        }
      }
    }
    valid_actions_cache_ = std::move(valid_actions); // Update the mutable cache
  }

  int GameStateCpp::get_current_step() const { return current_step_; }
  std::optional<std::string> GameStateCpp::get_game_over_reason() const { return game_over_reason_; }

  // Python-facing copy method uses the C++ copy constructor
  GameStateCpp GameStateCpp::copy() const
  {
    return GameStateCpp(*this);
  }

  void GameStateCpp::debug_toggle_cell(int r, int c)
  {
    if (grid_data_.is_valid(r, c) && !grid_data_.is_death(r, c))
    {
      auto &occupied_grid = grid_data_.get_occupied_grid_mut();
      auto &color_grid = grid_data_.get_color_id_grid_mut();
      bool was_occupied = occupied_grid[r][c];
      occupied_grid[r][c] = !was_occupied;
      color_grid[r][c] = was_occupied ? NO_COLOR_ID : DEBUG_COLOR_ID;
      if (!was_occupied)
      {
        // Check for line clears only if a cell becomes occupied
        grid_logic::check_and_clear_lines(grid_data_, {{r, c}});
      }
      invalidate_action_cache(); // Always invalidate after manual change
      // Force recalculation of valid actions and game over state after toggle
      get_valid_actions(true);
    }
  }

  void GameStateCpp::debug_set_shapes(const std::vector<std::optional<ShapeCpp>> &new_shapes)
  {
    size_t num_to_copy = std::min(new_shapes.size(), shapes_.size());
    for (size_t i = 0; i < num_to_copy; ++i)
    {
      shapes_[i] = new_shapes[i];
    }
    for (size_t i = num_to_copy; i < shapes_.size(); ++i)
    {
      shapes_[i] = std::nullopt;
    }
    invalidate_action_cache();
    // Force recalculation of valid actions and game over state after setting shapes
    get_valid_actions(true);
  }

  Action GameStateCpp::encode_action(int shape_idx, int r, int c) const
  {
    int grid_size = config_.rows * config_.cols;
    // Basic bounds check (more robust check in can_place)
    if (shape_idx < 0 || shape_idx >= config_.num_shape_slots || r < 0 || r >= config_.rows || c < 0 || c >= config_.cols)
    {
      // This case should ideally not be reached if called after can_place
      // Return an invalid action index or throw? Let's throw for internal logic errors.
      throw std::out_of_range("encode_action arguments out of range during valid action calculation.");
    }
    return shape_idx * grid_size + r * config_.cols + c;
  }

  std::tuple<int, int, int> GameStateCpp::decode_action(Action action) const
  {
    int action_dim = config_.num_shape_slots * config_.rows * config_.cols;
    if (action < 0 || action >= action_dim)
    {
      throw std::out_of_range("Action index out of range: " + std::to_string(action));
    }
    int grid_size = config_.rows * config_.cols;
    int shape_idx = action / grid_size;
    int remainder = action % grid_size;
    int r = remainder / config_.cols;
    int c = remainder % config_.cols;
    return {shape_idx, r, c};
  }

} // namespace trianglengin::cpp