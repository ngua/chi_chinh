import React from 'react';

class Categories extends React.Component {
  filterCategories = (category) => {
    this.props.filterCategories(category);
  }

  clearFilters = () => {
    this.props.clearFilters();
  }

  render() {
    const langCode = JSON.parse(document.querySelector('#lang').textContent)
    const selected = this.props.selected;
    const categories = this.props.categories;
    return (
      <ul className="uk-nav uk-nav-default uk-nav-parent-icon" uk-nav="true">
        <li className="uk-parent"><a className="parent">Filter by Category</a>
          <ul className="uk-nav-sub">
            { categories.map((category, i) => {
              const current = selected.includes(category);
              return (
                <li key={i}>
                  <a
                    name={category}
                    className={`child ${current ? ('active') : ''}`}
                    onClick={() => this.filterCategories(category) }
                  >
                    { category }
                  </a>
                </li>
              )}
            )}
          </ul>
        </li>
        <li>
          <a onClick={(e) => this.clearFilters()} className="parent">Clear All</a>
        </li>
        <li><a className="parent" href={`${window.origin}/${langCode}/recipes/archive/`}>Archive</a></li>
      </ul>
    )
  }

}

export default Categories;
