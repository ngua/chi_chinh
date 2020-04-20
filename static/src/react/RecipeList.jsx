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
      categories: null,
      loaded: false,
      error: false
    }
  }
  componentDidMount() {
    axios.get('/recipes/')
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return {error: true}
          })
        }
        const recipes = response.data;
        console.log(recipes);
        const allCategories = [...recipes.map(recipe => recipe.categories)].flat();
        const categories = Array.from(new Set(allCategories));
        this.setState(() => {
          return {
            categories: categories,
            recipes: recipes,
            loaded: true
          };
        })
      });
  }

  render() {
    const {categories, loaded, recipes } = this.state;
    return (
      <>
        { loaded ?
            (
              <>
                <div className="uk-container uk-container-large">
                  <ul className="uk-subnav uk-flex uk-flex-center uk-padding-large-bottom">
                    { categories.map((category, i) => {
                      return (
                        <li key={i} className="">
                          <CategoryButton name={category} />
                        </li>
                      )}
                    )}
                  </ul>
                  <div
                    className="uk-grid uk-flex uk-flex-center uk-grid-medium uk-child-width-1-2@s uk-child-width-1-3@m uk-grid-match"
                    uk-grid="true"
                  >
                    { recipes.map(recipe => {
                      return <Recipe key={recipe.id} recipe={recipe} />
                    })}
                  </div>
                </div>
              </>
            ) : (
              <div className="uk-text-center uk-padding-large">
                <Loader type='Oval' color='#949494' height={100} width={100} />
              </div>
            )
        }
      </>
    )
  }
}

export default RecipeList;
