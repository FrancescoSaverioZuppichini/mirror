import React, { Component } from 'react';
import './App.css';

import ModuleContainer from './ModuleContainer/ModuleContainer'
import { Provider, Subscribe } from 'unstated';
import Module from './Module/Module';

import AppBar from '@material-ui/core/AppBar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import Toolbar from '@material-ui/core/Toolbar';
import MenuIcon from '@material-ui/icons/Menu';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import { withStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';

import LayerOutputs from './Module/LayerOutputs/LayerOutputs'
const drawerWidth = 300;

const styles = theme => ({
  root: {
    flexGrow: 1,
    // height: 440,
    zIndex: 1,
    // overflow: 'hidden',
    position: 'relative',
    display: 'flex',
    minHeight: '100vh'
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawerPaper: {
    position: 'relative',
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    minWidth: 0, // So the Typography noWrap works
  },
  toolbar: theme.mixins.toolbar,

  progress: {
    position: 'absolute',
    top: '0',
    width: '100vw',
    zIndex: 9999
  },
})

function MyAppBar({ module, classes }) {
  return (
    <AppBar position="absolute" className={classes.appBar}>
      <Toolbar>
        <Typography variant="h6" color="inherit" noWrap>
          Mirror
      </Typography>
      </Toolbar>
    </AppBar>
  )
}

class App extends Component {

  render() {
    const classes = this.props.classes
    return (
      <Provider>
        <Subscribe to={[ModuleContainer]}>
          {module => (
            <div className={classes.root}>
              <MyAppBar module={MyAppBar} {...this.props} />

              <Drawer variant="permanent" classes={{
                paper: classes.drawerPaper,
              }}>
                <div className={classes.toolbar} />
                <Module module={module} />

              </Drawer>
              {module.state.isLoading ? (<LinearProgress color="secondary" className={classes.progress} />) : ''}

              <main className={classes.content}>
                <div className={classes.toolbar} />

                <LayerOutputs module={module} />
              </main>

            </div>
          )}
        </Subscribe>
      </Provider>
    );
  }
}


var StyledApp = withStyles(styles)(App);


export default StyledApp;
