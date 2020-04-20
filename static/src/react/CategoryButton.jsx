import React from 'react';

class CategoryButton extends React.Component {
  render() {
    return (
      <button className="uk-button uk-button-default uk-margin">
        { this.props.name }
      </button>
    )
  }
}

export default CategoryButton;
