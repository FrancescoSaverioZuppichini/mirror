import React, { Component } from 'react';
import './App.css';

import ModuleContainer from './ModuleContainer/ModuleContainer'
import { Provider, Subscribe } from 'unstated';
import Module from './Module/Module';
import Settings from './Settings/Settings'

import AppBar from '@material-ui/core/AppBar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import Toolbar from '@material-ui/core/Toolbar';
import MenuIcon from '@material-ui/icons/Menu';
import Drawer from '@material-ui/core/Drawer';
import { withStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';

import LayerOutputs from './Module/LayerOutputs/LayerOutputs'
import MoreIcon from '@material-ui/icons/MoreVert';

import Hidden from '@material-ui/core/Hidden';
import Inputs from './Inputs/Inputs';

const drawerWidth = 300;

const styles = theme => ({
  root: {
    flexGrow: 1,
    // height: 440,
    // zIndex: 1,
    // overflow: 'hidden',
    // position: 'relative',
    display: 'flex',
    flexDirection : 'row',
    minHeight: '100vh'
  },
  typography: {
    useNextVariants: true,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    flexShrink: 0,

    // position: 'relative',
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    // marginLeft: '300px',
    // position: 'fixed',
    // width: '100%',
    // height: '100%',
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    marginBottom: '102px'
    // minWidth: 0, // So the Typography noWrap works
  },
  toolbar: theme.mixins.toolbar,

  progress: {
    position: 'fixed',
    top: '0',
    width: '100vw',
    zIndex: 9999
  },

  settings: {
    width: '300px !important'
  },

  sliders : {
    width: '200px !important'
  },

  layersOuput : {
  },

  inputsBar : {
    position: 'fixed',
    bottom: 0,
    width: '100%',
    left: 0,
    overflowY:'scroll'
    // padding: theme.spacing.unit * 2,
  }
  
})

function MyAppBar({ module, classes }) {
  return (
    <AppBar position="fixed" className={classes.appBar}>
      <Toolbar>
        <Typography variant="h6" color="inherit" noWrap>
          Mirror
      </Typography>
      <div style={{flexGrow: 1}} ></div>
      <Hidden mdUp>
        <IconButton color="inherit" onClick={module.toogleDrawer}>
          <MoreIcon />
        </IconButton>
        </Hidden>

      </Toolbar>
    </AppBar>
  )
}

class App extends Component {
  state = {
    openSettings: false

  }


  toggleSettings = () => {
    const openSettings = !this.state.openSettings
    this.setState({ openSettings })
  }

  render() {
    const { classes } = this.props
    return (
      <Provider>
        <Subscribe to={[ModuleContainer]}>
          {module => (
            <div className={classes.root}>
              <MyAppBar module={MyAppBar} {...this.props} module={module} />

              <Drawer variant="permanent"
                      className={classes.drawer}

              classes={{
                paper: classes.drawerPaper,
              }}>
                <div className={classes.toolbar} />
                <Module module={module} />
              </Drawer>

              {module.state.isLoading ? (<LinearProgress color="secondary" className={classes.progress} />) : ''}

              <main className={classes.content}>
                <div className={classes.toolbar} />
                <LayerOutputs module={module} classes={classes}/>
                <Inputs module={module} classes={classes}></Inputs>
              </main>
                <Hidden smDown >
              <Settings
                toogle={module.toogleDrawer}
                open={module.state.open}
                module={module} 
                classes={classes}/>
                  </Hidden>

              <Hidden mdUp>
                <Settings
                toogle={module.toogleDrawer}
                open={module.state.open}
                module={module} 
                classes={classes}
                small={true}/>
              </Hidden>
            </div>
          )}
        </Subscribe>
      </Provider>
    );
  }
}


var StyledApp = withStyles(styles)(App)


export default StyledApp
