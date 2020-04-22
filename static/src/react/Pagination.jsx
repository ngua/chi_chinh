import React from 'react';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

class Pagination extends React.Component {
  getPageRange(currentPage, totalPages, offset) {
    if (currentPage < offset) {
      return totalPages.slice(0, offset)
    } else if (totalPages - currentPage < offset) {
      return totalPages.slice(-offset)
    }
    return totalPages.slice(currentPage - offset, currentPage + (offset - 1))
  }

  renderBeginEndArrow(orientation, page, selection) {
    return (
      <li><a
        uk-icon={`icon: chevron-double-${orientation}; ratio: 1.3`}
        onClick={() => this.props.fetchRecipes({params: {categories: selection, page: page}})}
      /> </li>
    )
  }

  renderPrevNextArrow(orientation, url) {
    return (
      <li><a>
        <span
          uk-icon={`icon: chevron-${orientation}; ratio: 1.1`}
          className="uk-margin-remove"
          onClick={() => this.props.fetchRecipes({url: url})}
        />
      </a></li>
    )
  }

  render() {
    const {currentPage, previous, next, selected, numPages, offset} = this.props;
    const totalPages = [...Array(numPages)].map((_, i) => i+1);
    const selection = selected.join(',');
    const pageRange = this.getPageRange(currentPage, totalPages, offset);
    const currentLimit = pageRange[pageRange.length - 1]
    const start = pageRange[0]
    return (
      <ul className="uk-pagination uk-flex-center">
        { numPages > 1 < start && this.renderBeginEndArrow('left', 1, selection) }
        { previous !== null && this.renderPrevNextArrow('left', previous) }
        { currentPage > offset && <span>...</span> }
        { pageRange.map(i => {
          const isCurrent = i === currentPage;
          return (
            <li key={i} className={ isCurrent ? 'uk-active' : ''} >
              <a onClick={() => this.props.fetchRecipes({params: {categories: selection, page: i}})} >{i}</a>
            </li>
          )
        }) }
        { currentLimit < numPages && <span>...</span>}
        { next !== null && this.renderPrevNextArrow('right', next) }
        { numPages > 1 && currentLimit < numPages && this.renderBeginEndArrow('right', numPages, selection)}
      </ul>
    )
  }
}

export default Pagination;
