#pragma once

//-----------------------------------------------------------------------------
// Common::CircularBuffer
//-----------------------------------------------------------------------------
namespace Common
{
template<typename T, unsigned int Size>
class CircularBuffer
{
public:
  CircularBuffer() : m_Input(Size - 1), m_Output(0)
  {
  }

  //-----------------------------------------------------------------------------
  // Public API
  //-----------------------------------------------------------------------------
  unsigned int GetUnallocated() const
  {
    return ((m_Input - m_Output) % Size);
  }

  unsigned int GetAllocated() const
  {
    return ((m_Output - m_Input - 1) % Size);
  }

  bool NonEmpty() const
  {
    return (GetAllocated() > 0);
  }

  bool NonFull() const
  {
    return (GetUnallocated() > 0);
  }

  bool Push(T key)
  {
    bool success = NonFull();
    if (success)
    {
      m_Buffer[m_Input] = key;
      m_Input = (m_Input - 1) % Size;
    }

    return success;
  }

  bool Pop(T &e)
  {
    bool success = NonEmpty();
    if (success)
    {
      m_Output = (m_Output - 1) % Size;
      e = m_Buffer[m_Output];
    }

    return success;
  }

private:
  //-----------------------------------------------------------------------------
  // Members
  //-----------------------------------------------------------------------------
  T m_Buffer[Size];
  unsigned int m_Input;
  unsigned int m_Output;

};
} // Common