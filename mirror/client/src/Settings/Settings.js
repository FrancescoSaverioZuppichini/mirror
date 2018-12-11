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
import {debounce} from 'throttle-debounce';


class VisualisationSettings extends Component{

    update = (value) => {
        var param = {...this.props.param, ...value}
        // console.log('value', value)
        // console.log('this.props.visualisation,', this.props.param)
        // console.log('visualisation,', param)
        const key = this.props.name
        var fromDown =  {}
        fromDown[key] = param
        this.props.update( fromDown)
    }

    makeParam = (param) => {
        if(param.type == 'slider') {
            var { max, min, step, value } = param
            return  (
                <ListItemText>
                    <div>{this.props.name + ' : ' + value}</div>
                    <div className={this.props.classes.sliders}>
                    <Slider
                        value={value}
                        aria-labelledby="label"
                        min={min}
                        max={max}
                        step={step}
                        onChange={debounce(300, (e, v) => this.update({...param,  ...{value : v}})) }
                    />
                    </div>
                </ListItemText>)
        }

        if(param.type == 'radio') {
            return   (
                <ListItemText>
                    <div>{this.props.name}</div>
                    <Radio
                    checked={param.value}
                    onChange={(e, v) => this.update({...param,  ...{value : !param.value}}) }
                    value="a"
                    name="radio-button-demo"
                    aria-label="A"
                    />
                </ListItemText>)
        }
    }

    render(){
        const { classes, module, param, name} = this.props
        const {params} = param

        return (
            <List>
                <ListItem>
                    {this.makeParam(param)}
                </ListItem>
                <ListItem>
                </ListItem>
                
            </List>
        )
    }
}

class VisualisationSettingsRoot extends Component {
    update = (value, down=true) => {
        console.log('from down', value)
        
        if(down) {
            var visualisation = {...this.props.visualisation.params, ...value}
            visualisation = {...this.props.visualisation, params: visualisation}
        } else{
            visualisation = {...this.props.visualisation, ...value}
        }
        console.log(visualisation)
        this.props.module.setVisualisationsSettings(visualisation)
        this.props.module.getLayerOutputs(this.props.module.state.layer, true)

    }

    render(){
        const { module, visualisation} = this.props
        const { name, params} = visualisation

        return (
            <List>
                <ListItem>
                    <ListItemText>
                    <div>{name}</div>
                    </ListItemText>
                    <Radio
                    checked={this.props.module.state.currentVisualisation.name == name}
                    onChange={(e, v) => this.update({...visualisation, value:v }, false) }
                    value="a"
                    name="radio-button-demo"
                    aria-label="A"
                    />
                </ListItem>
                    {Object.keys(params).map((k, i) => (<VisualisationSettings 
                    {...this.props}
                    name={k}
                    param={params[k]} 
                    update={this.update}
                    key={i}/>))}
            </List>
        )
    }
}


class Settings extends Component {
    componentDidMount(){
        this.props.module.getVisualisations()
    }

    onVisualisationSettingsChange = (data) => {
        this.props.module.setVisualisationsSettings(data)
    }

    handleSlider = (e, size) => {
        const { module } = this.props
        var settings = module.state.settings

        settings = Object.assign({}, settings, { size })

        module.changeSettings(settings)
    }


    render() {
        const { toogle, classes, open, module, small=false } = this.props
        return (
            <Drawer anchor="right"
                variant={small ? 'temporary' : 'permanent'} 
                open={open}
                className={classes.drawer}
                onClose={toogle}
                classes={{
                    paper: classes.drawerPaper,
                  }}
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
                            min={1}
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
                        {this.props.module.state.visualisations.map((v,i)=> <VisualisationSettingsRoot 
                        key={i}
                        {...this.props} 
                        visualisation={v} 
                        update={this.onVisualisationSettingsChange}/>)}
                  </ListItemText>
                  </ListItem>

                  </List>
            </Drawer>
        )
    }

}

export default Settings