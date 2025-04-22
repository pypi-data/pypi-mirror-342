#pragma once
#include "asgard_pde.hpp"
#include "asgard_permutations.hpp"

namespace asgard::elements
{
// yield single-d linear index for level/cell combo
int64_t get_1d_index(int const level, int const cell);

// yield level/cell for a single-d index
std::array<int64_t, 2> get_level_cell(int64_t const single_dim_id);

// mapping functions -- conceptually private/component local, exposed for
// testing return the linear index given element coordinates
int64_t map_to_id(fk::vector<int> const &coords, int const max_level,
                  int const num_dims);

// return the element coordinates given linear index
fk::vector<int>
map_to_coords(int64_t const id, int const max_level, int const num_dims);

// -----------------------------------------------------------------------------
// element table
// this object's purpose is:
// - to maintain a list of active element IDs
// - to provide a mapping from an assigned index (ordering) of an elements
//   to its coordinates
// - store a flattened version of this for access on devie
//
// about coordinates
// - coordinates are composed of a set of dimension-many pairs (level, cell).
//   (technically, an element's coordinates will also have a degree component,
//   but we omit this as we assume uniform degree).
// - in our table, coordinates are stored with all level components grouped,
//   followed by cell components so that a single coordinate will look like
//   e.g.: (lev_1, lev_2, ..., lev_dim, cell_1, cell_2, ..., cell_dim).
//
// re: full and sparse grid
// - to build a full grid, all potentional level combinations are included in
//   the table; that is, all dimension-length permutations of integers less
//   than or equal to the number of levels selected for the simulation are
//   valid components.
// - to build a sparse grid, we apply some rule to omit some of these
//   permutations. currently, we cull level combinations whose sum is greater
//   than the number of levels selected for the simulation.
// -----------------------------------------------------------------------------

class table
{
public:
  table() = default;

  table(int const max_level, prog_opts const &options);

  template<typename P>
  table(PDE<P> const &pde)
      : table(pde.max_level(), pde.options())
  {}

  // get id of element given its 0,...,n index in active elements
  int64_t get_element_id(int64_t const index) const
  {
    expect(index >= 0);
    expect(index < static_cast<int64_t>(active_element_ids_.size()));
    return active_element_ids_[index];
  }

  // lookup coords by index
  fk::vector<int> const &get_coords(int64_t const index) const
  {
    expect(index >= 0);
    expect(index < size());
    return id_to_coords_.at(active_element_ids_[index]);
  }

  // these functions return a  mapping new_indices -> old_indices
  // remove elements by index.
  void remove_elements(std::vector<int64_t> const &element_indices);

  // manually add elements by id
  // returns number of elements added - ignore ids already present
  int64_t
  add_elements(std::vector<int64_t> const &element_ids);

  // get element id of all children of an element (by index) for refinement
  std::list<int64_t>
  get_child_elements(int64_t const index,
                     std::vector<int> const &max_adapt_level) const;

  // get flattened element table for device
  fk::vector<int> const &get_active_table() const { return active_table_; }

  // returns the number of (active) elements in table
  int64_t size() const
  {
    expect(active_element_ids_.size() == id_to_coords_.size());
    return active_element_ids_.size();
  }

  void recreate_from_elements(std::vector<int64_t> const &element_ids);

  vector2d<int> get_cells() const
  {
    int const *const asg_idx = active_table_.data();
    int64_t const num_cells  = active_element_ids_.size();
    if (num_cells == 0)
      return vector2d<int>{};
    return asg2tsg_convert(id_to_coords_.begin()->second.size() / 2, num_cells, asg_idx);
  }

  // static construction helper
  // conceptually private, exposed for testing
  // return the cell indices given a level tuple
  static fk::matrix<int> get_cell_index_set(fk::vector<int> const &levels);

private:
  // ordering of active elements
  std::vector<int64_t> active_element_ids_;

  // map from element id to coords
  std::unordered_map<int64_t, fk::vector<int>> id_to_coords_;

  // table of active elements staged for on-device kron list building
  fk::vector<int> active_table_;

  int max_level_ = 1; // needed for coord translation
};

} // end namespace asgard::elements
