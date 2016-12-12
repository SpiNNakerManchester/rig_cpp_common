#pragma once

// Forward declarations
namespace Common
{
  namespace Random
  {
    class MarsKiss64;
  }
}

// Namespaces
using namespace Common::Random;

//-----------------------------------------------------------------------------
// Common::Maths
//-----------------------------------------------------------------------------
namespace Common
{
namespace Maths
{
  unsigned int Hypergeom(unsigned int ngood, unsigned int nbad, unsigned int nsample,
                         MarsKiss64 &rng);
} // Maths
} // Common
