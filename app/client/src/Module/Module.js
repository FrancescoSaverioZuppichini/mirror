import React, { Component } from 'react'
import Layer from './Layer/Layer';

export default class Module extends Component {
    componentDidMount(){
        this.props.module.getTree()
    }


    render() {
        var tree = this.props.module.state.tree

        return (
        <div>
            <Layer layer={tree}/>
        </div>
        )
    }
}
