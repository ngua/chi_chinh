import React from 'react';
import * as yup from 'yup';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Formik, Form, Field, useField } from 'formik';
import { gettext as _ } from 'django';

axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

const CSRFToken = () => {
  const csrf = Cookies.get('csrftoken');
  return (
    <input type="hidden" name="csrftoken" value={csrf} />
  )
}

const WrappedFormComponent = ({ WrappedComponent, ...props }) => {
  const [field, meta] = useField(props);
  return(
    <div className="uk-margin field">
      <div className="uk-form-controls">
        <WrappedComponent
          { ...field }
          { ...props }
          meta={meta}
          field={field}
        />
        { meta.touched && meta.error ? (
          <div className="uk-text-danger">{meta.error}</div>
        ) : (null
        )}
      </div>
    </div>
  )
}

const InputComponent = (props) => {
  return (
    <input
      { ...props.field }
      { ...props }
      className={`uk-input ${props.meta.touched && props.meta.error ? 'uk-form-danger' : ''}`}
    />
  )
}

const TextAreaComponent = (props) => {
  return  (
    <textarea
      { ...props.field }
      { ...props }
      className={`uk-textarea ${props.meta.touched && props.meta.error ? 'uk-form-danger' : ''}`}
    />
  )
}

const ContactFormComponent = (props) => {
  const handleError = () => {
    return props.errorHandler();
  }

  const handleSucces = () => {
    return props.successHandler();
  }

  const requiredMsg = _('This field is required')

  return (
    <Formik
      initialValues={{ name: '', email: '', message: '', phone: '' }}
      validationSchema={
        yup.object({
          name: yup.string().max(255, _('255 Characters or less')).required(requiredMsg),
          email: yup.string().email(_('Please enter a valid email address')).required(requiredMsg),
          message: yup.string().required(requiredMsg)
        })
      }
      onSubmit={(values, { setSubmitting }) => {
        setTimeout(() => {
          axios({
            method: 'POST',
            url: `${window.origin}/contact/api/`,
            data: JSON.stringify(values),
            headers: {
              'content-type': 'application/json'
            }
          })
            .then((response) => {
              if (response.status === 201) {
                handleSucces();
              } else {
                handleError();
              }
            })
              .catch(err => {
                handleError();
              });
          setSubmitting(false);
        }, 400);
      }}
    >
      <Form className="uk-form-stacked uk-width-4-5">
        <WrappedFormComponent
          WrappedComponent={InputComponent}
          placeholder={_('Name')}
          name='name'
          type='text'
        />
        <WrappedFormComponent
          WrappedComponent={InputComponent}
          placeholder={_('Email')}
          name='email'
          type='text'
        />
        <WrappedFormComponent
          WrappedComponent={TextAreaComponent}
          placeholder={_('Message')}
          name='message'
          rows={5}
        />
        <CSRFToken />
        <Field type="text" id="phone" name="phone" placeholder="Please enter your phone" />
        <button type="submit" className="uk-button uk-button-default">{_('Submit')}</button>
      </Form>
    </Formik>
  )
}

export default ContactFormComponent;
