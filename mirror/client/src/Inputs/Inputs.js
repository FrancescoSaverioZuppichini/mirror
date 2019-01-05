import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import classNames from 'classnames';

import { withStyles } from '@material-ui/core/styles';
import { Paper } from '@material-ui/core';

const styles = {
    inputImg : {
        width: '96px',
        height: '96px'
    },
    inputImgActive: {
        borderBottom: '3px rgb(53, 81, 181) solid'
    }
}

var Input = ({module, id, src, classes}) => {
    const isActive = id == module.state.currentInput
    return (
        <Grid item>
        <img className={classNames(classes.inputImg, 
                        {[classes.inputImgActive] :isActive  })}
            src={src} onClick={() => module.setInput(id)}>
            </img>
        </Grid>
    )
}

Input = withStyles(styles)(Input)

export default class Inputs extends Component {
    componentDidMount(){
        this.props.module.getInputs()
    }
    
    render() {
        const {classes} = this.props
        return (
            <Paper className={classes.inputsBar}>
                <Grid
                    container
                    direction="row"
                    justify="center"
                    alignItems="center"
                    spacing={4}
                    >
                {this.props.module.state.inputs.map((src, id) => 
                    (<Input src={src} id={id} {...this.props} key={id}></Input>))
                    }
                </Grid>   
            </Paper>
        )
    }
}