import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Grid from '@material-ui/core/Grid';
const Image = ({ src }) => {
    const style = {
        // backgroundImage : `url(${src})`,
        // backgroundSize: 100% 100%,
        height: '250px',
        width: '250px'
    }

    return  (<Grid item>
        <img style={style} src={src}></img>
    </Grid>)
}

const LayerOutputs = ({ module }) => (
    <Grid
        container
        direction="row"
        justify="center"
        alignItems="center"
        spacing={8}
    >
        {module.state.outputs.map((link, i) => <Image src={link} key={i}></Image>)}
    </Grid>
)
export default LayerOutputs