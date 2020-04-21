import React from 'react';
import axios from 'axios';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css'
import Loader from 'react-loader-spinner';
import CategoryButton from './CategoryButton';
import Recipe from './Recipe';

axios.defaults.baseURL = `${window.origin}/api/`;

class RecipeList extends React.Component {
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
        selected = state.selected.filter(item => item != category);
      } else {
        selected = [...state.selected, category];
      }
      return ({
        selected: selected
      })
    }, () => {
      const selection = this.state.selected.join(',');
      this.fetchRecipes({params: {categories: selection}});
    });
  }

  fetchPagination = (asboluteUrl) => {
    this.fetchRecipes({url: asboluteUrl});
  }

  componentDidMount() {
    this.fetchRecipes();
  }

  renderCategories(categories) {
    const selected = this.state.selected;
    return (
      <ul className="uk-subnav uk-flex uk-flex-center uk-padding-large-bottom">
        { categories.map((category, i) => {
            return (
              <li key={i} className="">
                <CategoryButton
                  name={category}
                  filterCategories={this.filterCategories}
                  current={this.state.selected.includes(category)}
                />
              </li>
            )}
          )}
      </ul>
    )
  }

  renderRecipes(recipes) {
    return (
      <div className="uk-grid uk-flex uk-flex-center uk-grid-medium uk-child-width-1-3@m uk-grid-match" uk-grid="true">
        { recipes.map(recipe => {
            return <Recipe key={recipe.id} recipe={recipe} />
          }) }
      </div>
    )
  }

  renderPaginationButtons(numPages) {
    const pageRange = [...Array(numPages)].map((_, i) => i+1);
    const {currentPage, previous, next} = this.state;
    const selection = this.state.selected.join(',');
    return (
      <ul className="uk-pagination uk-flex-center">
        { previous !== null && <li><a href="#">
            <span
              uk-pagination-previous="true"
              onClick={() => this.fetchPagination(previous)}
            />
          </a></li> }
        { pageRange.map(i => {
            const isCurrent = i === currentPage;
            return (
              <li key={i} className={ isCurrent ? 'uk-active' : ''} >
                <a href="#"
                  onClick={() => this.fetchRecipes({params: {categories: selection, page: i}})}
                >
                  {i}
                </a>
              </li>
            )
          }) }
        { next !== null && <li><a href="#">
            <span
              uk-pagination-next="true"
              onClick={() => this.fetchPagination(next)}
            />
          </a></li> }
      </ul>
    )
  }

  render() {
    const {categories, loaded, recipes, numPages } = this.state;
    return (
      <>
        { loaded ?
            (
              <>
                <div className="uk-container uk-container-large">
                  { this.renderCategories(categories) }
                  { this.renderRecipes(recipes) }
                  { this.renderPaginationButtons(numPages) }
                </div>
              </>
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
