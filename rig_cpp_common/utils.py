# Import modules
import struct

# Import classes
from collections import Iterable, namedtuple

# Import functions
from six import iteritems, iterkeys

# ----------------------------------------------------------------------------
# Args
# ----------------------------------------------------------------------------
class Args(namedtuple("Args", "args, kwargs")):
    def __new__(cls, *args, **kwargs):
        return super(Args, cls).__new__(cls, args, kwargs)

# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------
def load_regions(regions, region_arguments, machine_controller, core, logger):
    # Calculate region size
    size, allocs = sizeof_regions_named(regions, region_arguments)

    logger.debug("\t\t\t\t\tRegion size = %u bytes", size)

    # Allocate a suitable memory block
    # for this vertex and get memory io
    # **NOTE** this is tagged by core
    memory_io = machine_controller.sdram_alloc_as_filelike(
        size, tag=core.start)
    logger.debug("\t\t\t\t\tMemory with tag:%u begins at:%08x",
                    core.start, memory_io.address)

    # Layout the slice of SDRAM we have been given
    region_memory = create_app_ptr_and_region_files_named(
        memory_io, regions, region_arguments)

    # Write each region into memory
    for key, region in iteritems(regions):
        # Get memory
        mem = region_memory[key]

        # Get the arguments
        args, kwargs = region_arguments[key]

        # Perform the write
        region.write_subregion_to_file(mem, *args, **kwargs)

    # Return region memory
    return region_memory

def create_app_ptr_and_region_files_named(fp, regions, region_args):
    """Split up a file-like view of memory into smaller views, one per region,
    and write into the first region of memory the offsets to these later
    regions.

    Parameters
    ----------
    regions : {name: Region, ...}
        Map from keys to region objects.  The keys MUST support `int`, items
        from :py:class:`enum.IntEnum` are recommended.
    region_args : {name: (*args, **kwargs)}
        Map from keys to the arguments and keyword-arguments that should be
        used when determining the size of a region.

    Returns
    -------
    {name: file-like}
        Map from region name to file-like view of memory.
    """
    # Determine the number of entries needed in the application pointer table
    ptr_len = max(int(k) for k in iterkeys(regions)) + 1

    # Construct an empty pointer table of the correct length
    ptrs = [0] * ptr_len

    # Update the offset and then begin to allocate memory
    region_memory = dict()
    offset = (ptr_len * 4) + 4  # 1 word per region and magic number
    for k, region in iteritems(regions):
        # Get the size of this region
        args, kwargs = region_args[k]
        region_size = region.sizeof_padded(*args, **kwargs)

        # Store the current offset as the pointer for this region
        ptrs[int(k)] = offset

        # Get the memory region and update the offset
        next_offset = offset + region_size
        region_memory[k] = fp[offset:next_offset]
        offset = next_offset

    # Write the pointer table into memory
    fp.seek(0)
    fp.write(struct.pack("<{}I".format(1 + ptr_len), 0xAD130AD6, *ptrs))
    fp.seek(0)

    # Return the region memories
    return region_memory


def sizeof_regions_named(regions, region_args, include_app_ptr=True):
    """Return the total amount of memory required to represent
    all regions when padded to a whole number of words each
    and dictionary of any any extra allocations required

    Parameters
    ----------
    regions : {name: Region, ...}
        Map from keys to region objects.  The keys MUST support `int`, items
        from :py:class:`enum.IntEnum` are recommended.
    region_args : {name: (*args, **kwargs)}
        Map from keys to the arguments and keyword-arguments that should be
        used when determining the size of a region.
    """
    if include_app_ptr:
        # Get the size of the application pointer
        size = 4 + ((max(int(k) for k in iterkeys(regions)) + 1) * 4)
    else:
        # Don't include the application pointer
        size = 0

    # Get the size of all the regions
    allocations = {}
    for key, region in iteritems(regions):
        # Get the arguments for the region
        args, kwargs = region_args[key]

        # Get size of region and any extra allocations it requires
        region_size_allocs = region.sizeof_padded(*args, **kwargs)

        # Add size to total and include allocations in dictionary
        if isinstance(region_size_allocs, Iterable):
            size += region_size_allocs[0]
            allocations.update(region_size_allocs[1])
        else:
            size += region_size_allocs

    return size, allocations