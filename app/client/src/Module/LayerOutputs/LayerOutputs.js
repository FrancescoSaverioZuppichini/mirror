import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Grid from '@material-ui/core/Grid';

import Slider from '@material-ui/lab/Slider';

const Image = ({ src, size }) => {
    const style = {
        // backgroundImage : `url(${src})`,
        // backgroundSize: 100% 100%,
        height: `${100 * (size/20)}px`,
        width: `${100 * (size/20)}px`
    }

    return (<Grid item>
        <img style={style} src={src}></img>
    </Grid>)
}

class LayerOutputs extends React.Component {
    state = {
        value: 50,
    };

    handleChange = (event, value) => {
        this.setState({ value });
    }

    render() {
        const module = this.props.module
        
        return (
            <Grid
                container
                direction="row"
                justify="flex-start"
                alignItems="left"
                spacing={8}
            >
        <Grid item xs={12}>
                      <Slider
            value={this.state.value}
            aria-labelledby="label"
            onChange={this.handleChange}
          />
          {this.state.value}

          </Grid>
                {module.state.outputs.map((link, i) => <Image src={link} size={this.state.value} key={i}></Image>)}
            </Grid>
        )
    }
}
export default LayerOutputs