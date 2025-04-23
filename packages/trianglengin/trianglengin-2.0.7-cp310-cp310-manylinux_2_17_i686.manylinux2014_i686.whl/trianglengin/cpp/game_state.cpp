
// File: src/trianglengin/cpp/game_state.cpp
#include "game_state.h"
#include "grid_logic.h"
#include "shape_logic.h"
#include <stdexcept>
#include <numeric>
#include <iostream>
#include <algorithm> // For std::min

namespace trianglengin::cpp
{

  GameStateCpp::GameStateCpp(const EnvConfigCpp &config, unsigned int initial_seed)
      : config_(config),
        grid_data_(config_),
        shapes_(config_.num_shape_slots),
        score_(0.0),
        current_step_(0),
        last_cleared_triangles_(0), // Initialize added member
        game_over_(false),
        rng_(initial_seed)
  {
    reset();
  }

  // --- Explicit Copy Constructor ---
  GameStateCpp::GameStateCpp(const GameStateCpp &other)
      : config_(other.config_),
        grid_data_(other.grid_data_),
        shapes_(other.shapes_),
        score_(other.score_),
        current_step_(other.current_step_),
        last_cleared_triangles_(other.last_cleared_triangles_), // Copy added member
        game_over_(other.game_over_),
        game_over_reason_(other.game_over_reason_),
        valid_actions_cache_(other.valid_actions_cache_),
        rng_(other.rng_)
  {
  }

  // --- Explicit Copy Assignment Operator ---
  GameStateCpp &GameStateCpp::operator=(const GameStateCpp &other)
  {
    if (this != &other)
    {
      config_ = other.config_;
      grid_data_ = other.grid_data_;
      shapes_ = other.shapes_;
      score_ = other.score_;
      current_step_ = other.current_step_;
      last_cleared_triangles_ = other.last_cleared_triangles_; // Copy added member
      game_over_ = other.game_over_;
      game_over_reason_ = other.game_over_reason_;
      valid_actions_cache_ = other.valid_actions_cache_;
      rng_ = other.rng_;
    }
    return *this;
  }

  void GameStateCpp::reset()
  {
    grid_data_.reset();
    std::fill(shapes_.begin(), shapes_.end(), std::nullopt);
    score_ = 0.0;
    current_step_ = 0;
    last_cleared_triangles_ = 0; // Reset added member
    game_over_ = false;
    game_over_reason_ = std::nullopt;
    valid_actions_cache_ = std::nullopt;
    shape_logic::refill_shape_slots(*this, rng_);
    check_initial_state_game_over();
  }

  void GameStateCpp::check_initial_state_game_over()
  {
    get_valid_actions(true);
  }

  std::tuple<double, bool> GameStateCpp::step(Action action)
  {
    last_cleared_triangles_ = 0; // Reset before potential clearing

    if (game_over_)
    {
      return {0.0, true};
    }

    const auto &valid_actions = get_valid_actions();

    if (valid_actions.find(action) == valid_actions.end())
    {
      force_game_over("Invalid action provided: " + std::to_string(action));
      score_ += config_.penalty_game_over;
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
    shapes_[shape_idx] = std::nullopt;

    // --- Line Clearing ---
    int lines_cleared_count;
    std::set<Coord> cleared_coords;
    LineFsSet cleared_lines_fs;
    std::tie(lines_cleared_count, cleared_coords, cleared_lines_fs) =
        grid_logic::check_and_clear_lines(grid_data_, newly_occupied_coords);
    int cleared_count = static_cast<int>(cleared_coords.size());
    last_cleared_triangles_ = cleared_count; // Store cleared count

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
    invalidate_action_cache();
    get_valid_actions(true);

    // --- Calculate Reward & Update Score ---
    double reward = 0.0;
    reward += static_cast<double>(placed_count) * config_.reward_per_placed_triangle;
    reward += static_cast<double>(cleared_count) * config_.reward_per_cleared_triangle;

    if (game_over_)
    {
      // Penalty already applied if game over was due to invalid action this step.
    }
    else
    {
      reward += config_.reward_per_step_alive;
    }
    score_ += reward;

    return {reward, game_over_};
  }

  bool GameStateCpp::is_over() const
  {
    return game_over_;
  }

  void GameStateCpp::force_game_over(const std::string &reason)
  {
    if (!game_over_)
    {
      game_over_ = true;
      game_over_reason_ = reason;
      valid_actions_cache_ = std::set<Action>();
    }
  }

  double GameStateCpp::get_score() const
  {
    return score_;
  }

  const std::set<Action> &GameStateCpp::get_valid_actions(bool force_recalculate)
  {
    if (game_over_)
    {
      if (!valid_actions_cache_.has_value() || !valid_actions_cache_->empty())
      {
        valid_actions_cache_ = std::set<Action>();
      }
      return *valid_actions_cache_;
    }

    if (!force_recalculate && valid_actions_cache_.has_value())
    {
      return *valid_actions_cache_;
    }

    calculate_valid_actions_internal();

    if (!game_over_ && valid_actions_cache_->empty())
    {
      force_game_over("No valid actions available.");
    }

    return *valid_actions_cache_;
  }

  void GameStateCpp::invalidate_action_cache()
  {
    valid_actions_cache_ = std::nullopt;
  }

  void GameStateCpp::calculate_valid_actions_internal() const
  {
    std::set<Action> valid_actions;
    for (int shape_idx = 0; shape_idx < static_cast<int>(shapes_.size()); ++shape_idx)
    {
      if (!shapes_[shape_idx].has_value())
        continue;
      const ShapeCpp &shape = shapes_[shape_idx].value();
      for (int r = 0; r < config_.rows; ++r)
      {
        for (int c = 0; c < config_.cols; ++c)
        {
          if (grid_logic::can_place(grid_data_, shape, r, c))
          {
            valid_actions.insert(encode_action(shape_idx, r, c));
          }
        }
      }
    }
    valid_actions_cache_ = std::move(valid_actions);
  }

  int GameStateCpp::get_current_step() const { return current_step_; }
  int GameStateCpp::get_last_cleared_triangles() const { return last_cleared_triangles_; } // Added implementation
  std::optional<std::string> GameStateCpp::get_game_over_reason() const { return game_over_reason_; }

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
      last_cleared_triangles_ = 0; // Reset cleared count after manual toggle
      if (!was_occupied)
      {
        // Check for line clears only if a cell becomes occupied
        auto clear_result = grid_logic::check_and_clear_lines(grid_data_, {{r, c}});
        last_cleared_triangles_ = static_cast<int>(std::get<1>(clear_result).size());
      }
      invalidate_action_cache();
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
    get_valid_actions(true);
  }

  Action GameStateCpp::encode_action(int shape_idx, int r, int c) const
  {
    int grid_size = config_.rows * config_.cols;
    if (shape_idx < 0 || shape_idx >= config_.num_shape_slots || r < 0 || r >= config_.rows || c < 0 || c >= config_.cols)
    {
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