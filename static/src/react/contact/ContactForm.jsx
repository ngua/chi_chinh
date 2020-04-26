import React from 'react';
import { gettext as _ } from 'django';
import ContactFormComponent from './ContactFormComponent'

class ContactForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: false
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

  errorHandler() {
    this.setState({
      error: true
    });
  }

  render() {
    const error = this.state.error;
    return (
      <>
        { error ? (
          this.renderError()
        ) : (
          <ContactFormComponent errorHandler={() => this.errorHandler()}/>
        ) }
      </>
    )
  }
}

export default ContactForm;
