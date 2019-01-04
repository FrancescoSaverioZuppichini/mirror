import React, { Component } from 'react';

const Input = ({module, id, src}) => {
    return (
        <img src={src} onClick={() => module.setInput(id)}></img>
    )
}

export default class Inputs extends Component {
    componentDidMount(){
        this.props.module.getInputs()
    }
    
    render() {
        return (
            <div>
            {this.props.module.state.inputs.map((src, id) => 
                (<Input src={src} id={id} {...this.props} key={id}></Input>))
                }
            </div>   
        )
    }
}