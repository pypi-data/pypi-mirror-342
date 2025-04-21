// File: src/trianglengin/cpp/structs.h
#ifndef TRIANGLENGIN_CPP_STRUCTS_H
#define TRIANGLENGIN_CPP_STRUCTS_H

#pragma once

#include <vector>
#include <tuple>
#include <string>
#include <cstdint>
#include <utility> // For std::move

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
} // namespace trianglengin::cpp

#endif // TRIANGLENGIN_CPP_STRUCTS_H