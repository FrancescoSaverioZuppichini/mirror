import React, { Component } from 'react';

const Input = ({module, src}) => {
    return (
        <img src={src}></img>
    )
}

export default class Inputs extends Component {
    componentDidMount(){
        this.props.module.getInputs()
    }
    
    render() {
        return (
            <div>
            {this.props.module.state.inputs.map(el => 
                (<Input src={el} {...this.props}></Input>))
                }
            </div>   
        )
    }
}