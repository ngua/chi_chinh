import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

class Recipe extends React.Component {
  renderHeader(picture) {
    return (
      <div className="uk-card-header">
        <div className="uk-card-media-top">
          <img src={picture} alt="" height={400} width={400}/>
        </div>
      </div>
    )
  }

  renderBody(name, slug) {
    return (
      <div className="uk-grid uk-grid-small" uk-grid="true">
        <div className="uk-width-expand">
          <h3 className="heading uk-width-2-3 uk-card-title">
            {name}
          </h3>
        </div>
        <div className="uk-width-auto uk-text-right uk-text-muted">
          <a href={window.location + slug} className="uk-margin-right" ratio="1.2" uk-icon="chevron-double-right"/>
          <a href="#" className="uk-margin-right" ratio="1.2" uk-icon="youtube"/>
        </div>
      </div>
    )
  }

  render() {
    const recipe = this.props.recipe;
    const datePosted = new Date(recipe.created);
    return (
      <div className="uk-animation-fade">
        <div className="uk-card uk-card-medium uk-card-hover">
          { this.renderHeader(recipe.picture) }
          <div className="uk-card-body uk-padding-remove-top">
            { this.renderBody(recipe.name, recipe.slug) }
            <p className="uk-text-meta">Posted on { datePosted.toLocaleDateString() }</p>
            <hr />
            {recipe.categories.map((category, i) => {
              return (
                <div key={i} className="uk-label uk-margin-small-right">
                  {category}
                </div>
              )
            })}
          </div>
        </div>
      </div>
    )
  }
}

export default Recipe;
