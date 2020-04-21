import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

class Recipe extends React.Component {
  render() {
    const recipe = this.props.recipe;
    const datePosted = new Date(recipe.created);
    const categories = recipe.categories;
    return (
      <div className="uk-animation-fade">
        <div className="uk-card uk-card-medium uk-card-hover">
          <div className="uk-card-header">
            <div className="uk-card-media-top">
              <img src={recipe.picture} alt="" height={400} width={400}/>
            </div>
          </div>
          <div className="uk-card-body uk-padding-remove-top">
            <div className="uk-grid uk-grid-small" uk-grid="true">
              <div className="uk-width-expand">
                <h3 className="heading uk-width-2-3 uk-card-title">
                  {recipe.name}
                </h3>
              </div>
              <div className="uk-width-auto uk-text-right uk-text-muted">
                <a href="#" className="uk-margin-right" ratio="1.2" uk-icon="chevron-double-right"/>
                <a href="#" className="uk-margin-right" ratio="1.2" uk-icon="youtube"/>
              </div>
            </div>
            <p className="uk-text-meta">Posted on { datePosted.toLocaleDateString() }</p>
            <hr />
            {categories.map((category, i) => {
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
