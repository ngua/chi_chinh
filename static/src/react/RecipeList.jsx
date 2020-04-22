import React from 'react';
import axios from 'axios';
import Loader from 'react-loader-spinner';
import CategoryButton from './CategoryButton';
import Recipe from './Recipe';
import Pagination from './Pagination';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css'

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
      const selection = this.state.selected.join(',');
      this.fetchRecipes({params: {categories: selection}});
    });
  }

  componentDidMount() {
    this.fetchRecipes();
  }

  componentWillUnmount() {
    this.signal.cancel();
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
                  { numPages > 1 &&
                    <Pagination
                      {...this.state}
                      offset={3}
                      fetchRecipes={this.fetchRecipes}
                    /> }
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
