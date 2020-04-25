const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: {
    recipes: './react/recipes.jsx'
  },

  output: {
    path: path.resolve('./bundles/'),
    filename: '[name].js',
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
         use: [
           {
             loader: 'babel-loader'
           },
        ],
      },
      {
        test: /\.s?css$/i,
        loader: 'css-loader',
        options: {
          'import': true
        },
      },
    ],
  },

  resolve: {
    extensions: ['*', '.js', '.jsx']
  },

  externals: {
    django: 'django'
  },
}
