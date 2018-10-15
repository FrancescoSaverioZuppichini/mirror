import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Grid from '@material-ui/core/Grid';

import Slider from '@material-ui/lab/Slider';
import Button from '@material-ui/core/Button';

const Image = ({ src, size }) => {
    const style = {
        // backgroundImage : `url(${src})`,
        // backgroundSize: 100% 100%,
        height: `${100 * (size / 20)}px`,
        width: `${100 * (size / 20)}px`
    }

    return (<Grid item>
        <img style={style} src={src}></img>
    </Grid>)
}

class LayerOutputs extends React.Component {
    render() {
        const { module } = this.props

        return (
            <div>
                <Grid
                    container
                    direction="row"
                    justify="flex-start"
                    alignItems="center"
                    spacing={0}
                >
                    {module.state.outputs.map((link, i) =>
                        <Image src={link} {...module.state.settings} key={i}></Image>
                    )}

                </Grid>
                <Grid
                    container
                    direction="row"
                    justify="center"
                    alignItems="center"
                    spacing={8}
                >
                    <Grid item>
                        <Button variant="contained" color="primary" onClick={() => module.getLayerOutputs()}>
                            More
                    </Button>
                    </Grid>
                </Grid>
            </div>

        )
    }
}
export default LayerOutputs