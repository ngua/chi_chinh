import React from 'react';
import { gettext as _ } from 'django';
import ContactFormComponent from './ContactFormComponent'
import Loader from 'react-loader-spinner';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css'

class ContactForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: false,
      success: false
    }
  }

  renderError() {
    return (
      <>
        <div>
          <h1 className="heading">{ _("We're sorry, something went wrong.") }</h1>
          <p className="uk-text-muted">{ _('Please try to get in touch again.') }</p>
        </div>
      </>
    )
  }

  renderSuccess() {
    return (
      <>
        <div>
          <h1 className="heading">{ _('Thanks for getting in touch!') }</h1>
          <p className="uk-text-muted">{ _("We'll get back to you soon.") }</p>
          <Loader type='Oval' color='#949494' height={75} width={75} />
        </div>
      </>
    )
  }

  successHandler() {
    this.setState({
      success: true
    }, () => {
      setTimeout(() => {
        location.replace(window.origin);
      }, 5000);
    })
  }

  errorHandler() {
    this.setState({
      error: true
    });
  }

  render() {
    const { error, success } = this.state;
    return (
      <>
        { error ? (
          this.renderError()
        ) : success ? (
          this.renderSuccess()
        ) : (
          <ContactFormComponent errorHandler={() => this.errorHandler()} successHandler={() => this.successHandler()} />
        ) }
      </>
    )
  }
}

export default ContactForm;
