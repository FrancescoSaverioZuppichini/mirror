import React, { Component } from 'react'
import Layer from './Layer/Layer';
import List from '@material-ui/core/List';

export default class Module extends Component {
    componentDidMount(){
        this.props.module.getTree()
    }


    render() {
        var tree = this.props.module.state.tree

        return (
        <List>
            <Layer layer={tree} module={this.props.module} deepth={1}/>
        </List>
        )
    }
}
