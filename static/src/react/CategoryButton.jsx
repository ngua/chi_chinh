import React from 'react';

class CategoryButton extends React.Component {
  constructor(props) {
    super(props);
    this.filterCategories = this.filterCategories.bind(this);
  }

  filterCategories(category) {
    this.props.filterCategories(category);
  }

  render() {
    const category = this.props.name;
    return (
      <button
        className={`uk-button uk-margin ${this.props.current ? ('active') : 'uk-button-default '}`}
        onClick={() => this.filterCategories(category) }
      >
        { this.props.name }
      </button>
    )
  }
}

export default CategoryButton;
