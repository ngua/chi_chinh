import React from 'react';
import axios from 'axios';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';
import Loader from 'react-loader-spinner';
import Categories from './Categories';
import Recipe from './Recipe';
import Pagination from './Pagination';
import { gettext as _ } from 'django';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css'

UIkit.use(Icons);
axios.defaults.baseURL = `${window.origin}/api/`;

class RecipeList extends React.Component {
  signal = axios.CancelToken.source();

  constructor(props) {
    super(props);
    this.state = {
      recipes: [],
      categories: [],
      selected: [],
      currentPage: null,
      next: null,
      previous: null,
      numPages: null,
      count: null,
      loaded: false,
      error: false
    }
  }

  fetchRecipes = async ({url = '/recipes/', params = {}} = {}) => {
    axios.get(url, {
      params: params
    })
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return {error: true}
          })
        };
        const { all, count, next, previous, results, current, total } = response.data;
        const categories = [...all.map(all => all.name)];
        this.setState(() => {
          return {
            categories: categories,
            count: count,
            next: next,
            previous: previous,
            recipes: results,
            currentPage: current,
            numPages: total,
            loaded: true
          };
        })
      });
  }

  filterCategories = (category) => {
    this.setState((state) => {
      let selected;
      if (state.selected.includes(category)) {
        selected = state.selected.filter(item => item !== category);
      } else {
        selected = [...state.selected, category];
      }
      return ({
        selected: selected
      })
    }, () => {
      const selection = this.joinSelected();
      this.fetchRecipes({params: {categories: selection}});
    });
  }

  clearFilters = (e) => {
    this.setState({
      selected: [],
    }, () => {
      this.fetchRecipes();
    })
  }

  joinSelected() {
    return this.state.selected.join(',');
  }

  componentDidMount() {
    this.fetchRecipes();
  }

  componentWillUnmount() {
    this.signal.cancel();
  }

  renderRecipes(recipes) {
    if (recipes.length >= 1) {
      return (
        <div className="uk-grid uk-flex uk-flex-left uk-grid-medium uk-child-width-1-3@m uk-grid-match" uk-grid="true">
          { recipes.map(recipe => {
            return <Recipe key={recipe.id} recipe={recipe} />
          }) }
        </div>
      )
    }
    return (
      <div id="no-results" className="uk-grid uk-flex-center uk-child-width-1-1@m uk-background-muted" uk-grid="true">
        <div className="uk-container uk-padding-large uk-text-center uk-height-medium">
          <div>
            <h1 className="heading">{ _('No matching recipes found!') }</h1>
            <p>{ _('Try choosing another combination') }</p>
          </div>
        </div>
      </div>
    )
  }

  render() {
    const {categories, loaded, recipes, numPages } = this.state;
    return (
      <>
        { loaded ?  (
          <div className="uk-container uk-container-large">
            <div className="uk-grid uk-grid-divider" uk-grid="true">
              <div id="categories" className="uk-width-1-5@m sub-nav">
                <Categories
                  categories={this.state.categories}
                  selected={this.state.selected}
                  filterCategories={this.filterCategories}
                  clearFilters={this.clearFilters}
                />
              </div>
              <div className="uk-width-4-5@m">
                { recipes && this.renderRecipes(recipes) }
              </div>
            </div>
            { numPages > 1 &&
            <Pagination
              {...this.state}
              offset={3}
              fetchRecipes={this.fetchRecipes}
            /> }
            <div className="uk-flex uk-flex-center uk-hidden@m">
              <a href="#top" uk-totop="true" uk-scroll="true"/>
            </div>
          </div>
        ) : (
          <div className="uk-text-center uk-padding-large">
            <Loader type='Oval' color='#949494' height={100} width={100} />
          </div>
        ) }
      </>
    )
  }
}

export default RecipeList;
