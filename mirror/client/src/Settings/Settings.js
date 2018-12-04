import React, { Component } from 'react';

import Drawer from '@material-ui/core/Drawer';

import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

import Grid from '@material-ui/core/Grid';

import ModuleContainer from '../ModuleContainer/ModuleContainer'
import { Provider, Subscribe } from 'unstated';

import Slider from '@material-ui/lab/Slider';
import Radio from '@material-ui/core/Radio';

import { withStyles } from '@material-ui/core/styles';

class VisualisationSettings extends Component{
    state = {
        visualisation : null
    }

    componentDidMount(){
        this.setState({visualisation: this.props.visualisation})
    }

    render(){
        const { module, visualisation} = this.props
        const { name, properties} = visualisation
        
        return (
            <List>
                <ListItem>
                    <ListItemText>
                    <div>{name}</div>
                    <Radio
                    checked={module.state.currentVisualisation.name === name}
                    onChange={() => this.props.change(this.state.visualisation)}
                    value="a"
                    name="radio-button-demo"
                    aria-label="A"
                    />
                    </ListItemText>
                </ListItem>
            </List>
        )
    }
}



class Settings extends Component {
    componentDidMount(){
        this.props.module.getVisualisations()
    }

    handleSlider = (e, size) => {
        const { module } = this.props
        var settings = module.state.settings

        settings = Object.assign({}, settings, { size })
        console.log(settings)
        module.changeSettings(settings)
    }

    onVisualisationSettingsChange = (data) => {
        console.log('di0ocane')
        this.props.module.setVisualisationsSettings(data)
    }

    render() {
        const { toogle, classes, open, module } = this.props
        return (
            <Drawer anchor="right"
                open={open}
                onClose={toogle}
            >
                <div className={classes.toolbar} />
                <List className={classes.settings}>
                    <ListItem>
                        <ListItemText>
                            Image size : {module.state.settings.size}
                        </ListItemText>

                    </ListItem>
                    <ListItem>
                        <Slider
                            value={module.state.settings.size}
                            aria-labelledby="label"
                            min={0}
                            max={100}
                            step={1}
                            onChange={this.handleSlider}
                        />
                    </ListItem>
                </List>

                  <List className={classes.settings}>
                  <ListItem>

                  <ListItemText>
                  <div>Visualisations</div>
                        {this.props.module.state.visualisations.map((v,i)=> <VisualisationSettings 
                        key={i}
                        {...this.props} 
                        visualisation={v} 
                        change={this.onVisualisationSettingsChange}/>)}
                  </ListItemText>
                  </ListItem>

                  </List>
            </Drawer>
        )
    }

}

export default Settings