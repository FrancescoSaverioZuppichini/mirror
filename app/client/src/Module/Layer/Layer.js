import React, { Component } from 'react'

export default class Layer extends Component {
    renderLayer = (layer) => {
        const name = this.props.layer.name.split('(')[0]
        return (
            (<div>
                <h6>{name}</h6>
                {layer.children.map(el => (<Layer layer={el}>
                </Layer>))}
            </div>)
        )
    }

    render() {
        const layer = this.props.layer
        return (
            <div>
                {layer ? this.renderLayer(layer) : (<div></div>)}
            </div>
        )
    }
}
