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

  renderBody(name, url, absURL) {
    return (
      <div className="uk-grid uk-grid-small" uk-grid="true">
        <div className="uk-width-expand">
          <h3 className="heading uk-width-2-3 uk-card-title">
            {name}
          </h3>
        </div>
        <div className="uk-width-auto uk-text-right uk-text-muted">
          <a href={absURL} target="_blank" className="uk-margin-right" ratio="1.2" uk-icon="chevron-double-right"/>
          <a href={url} target="_blank" className="uk-margin-right" ratio="1.2" uk-icon="youtube"/>
        </div>
      </div>
    )
  }

  render() {
    const { name, created, picture, categories, url, absurl } = this.props.recipe;
    const dateCreated = new Date(created);
    return (
      <div className="uk-animation-fade">
        <div className="uk-card uk-card-medium uk-card-hover">
          { this.renderHeader(picture) }
          <div className="uk-card-body uk-padding-remove-top">
            { this.renderBody(name, url, absurl) }
            <p className="uk-text-meta">Posted on { dateCreated.toLocaleDateString() }</p>
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
