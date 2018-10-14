import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import ModuleContainer from './ModuleContainer/ModuleContainer'
import { Provider, Subscribe } from 'unstated';
import Module from './Module/Module';

class App extends Component {
  componentDidMount(){

  }

  render() {
    return (
      <Provider>
          <Subscribe to={[ModuleContainer]}>
          { module => (
          <Module module={module}/>
          )}
          </Subscribe>
      </Provider>
    );
  }
}

export default App;
