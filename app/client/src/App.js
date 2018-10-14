import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import ModuleContainer from './ModuleContainer/ModuleContainer'
import { Provider, Subscribe } from 'unstated';
import Module from './Module/Module';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import LinearProgress from 'material-ui/LinearProgress';
import Drawer from 'material-ui/Drawer';
import RaisedButton from 'material-ui/RaisedButton';
class App extends Component {
  componentDidMount() {

  }

  render() {
    return (
      <Provider>
        <Subscribe to={[ModuleContainer]}>
          {module => (
            <div>
              <AppBar
                title="Mirror"
                iconClassNameRight="muidocs-icon-navigation-expand-more"
                onLeftIconButtonClick={module.toogleDrawer}
              />
              <Drawer open={module.state.open}>
                <RaisedButton
                  label="Close"
                  onClick={module.toogleDrawer}
                />
                <Module module={module} />
              </Drawer>
              {module.state.isLoading ? (<LinearProgress />) : ''}
            </div>
          )}
        </Subscribe>
      </Provider>
    );
  }
}

const MuiAppp = () => (
  <MuiThemeProvider>
    <App />
  </MuiThemeProvider>
)

export default MuiAppp;
