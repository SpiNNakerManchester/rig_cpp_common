#pragma once

// Common includes
#include "../fixed_point_number.h"

// Forward declarations
namespace Common
{
  namespace Random
  {
    class MarsKiss64;
  }
}

// Namespaces
using namespace Common::FixedPointNumber;
using namespace Common::Random;

//-----------------------------------------------------------------------------
// Common::Maths
//-----------------------------------------------------------------------------
namespace Common
{
namespace Maths
{
  unsigned int Binomial(unsigned int n, S1615 p, MarsKiss64 &rng);

  unsigned int Binomial(unsigned int n, unsigned int numerator, unsigned int denominator,
                        MarsKiss64 &rng);
} // Maths
} // Common
