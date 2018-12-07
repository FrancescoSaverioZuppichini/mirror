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

    update = (value) => {
        var visualisation = {...this.props.visualisation, ...value}
     
        this.props.update({ params: [visualisation]})
    }

    makeParam = (param) => {
        if(param.type == 'slider') {
            var { max, min, value } = param
            return  (<Slider
                        value={value}
                        aria-labelledby="label"
                        min={min}
                        max={max}
                        step={0.1}
                        onChange={(e, v) => this.update({...param,  ...{value : v}}) }
                    />)
        }

        if(param.type == 'radio') {
            return   (<Radio
                    checked={param.value}
                    onChange={(e, v) => this.update({...param,  ...{value : !param.value}}) }
                    value="a"
                    name="radio-button-demo"
                    aria-label="A"
                    />)
        }
    }

    render(){
        const { module, visualisation} = this.props
        const { name, params} = visualisation
        console.log('render', visualisation)

        return (
            <List>
                <ListItem>
                    <ListItemText>
                    <div>{name}</div>
                    </ListItemText>
                    {this.makeParam(visualisation)}
                </ListItem>
                {params.map(p => (<VisualisationSettings visualisation={p} update={this.update}/>))}
            </List>
        )
    }
}

class VisualisationSettingsRoot extends Component {
    update = (value) => {
        var visualisation = {...this.props.visualisation, ...value}

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
                    onChange={(e, v) => this.update({...visualisation, value:v }) }
                    value="a"
                    name="radio-button-demo"
                    aria-label="A"
                    />
                </ListItem>
                {params.map(p => (<VisualisationSettings visualisation={p} update={this.update}/>))}
            </List>
        )
    }
}


class Settings extends Component {
    componentDidMount(){
        this.props.module.getVisualisations()
    }

    onVisualisationSettingsChange = (data) => {
        console.log('onVisualisationSettingsChange', data)
        this.props.module.setVisualisationsSettings(data.params[0])
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