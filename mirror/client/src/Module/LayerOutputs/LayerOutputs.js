import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Grid from '@material-ui/core/Grid';

import Slider from '@material-ui/lab/Slider';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

class AtomicImage  extends Component {
    constructor(props) {
         super(props);
         this.state = {dimensions: {}};
         this.onImgLoad = this.onImgLoad.bind(this);
     }
     onImgLoad({target:img}) {
         this.setState({dimensions:{height:img.offsetHeight,
                                    width:img.offsetWidth}});
     }
     render(){
         const {src, size} = this.props;
         const {width, height} = this.state.dimensions;
        
         const style = {
            // backgroundImage : `url(${src})`,
            // backgroundSize: 100% 100%,
            height: `${height * size}px`,
            width: `${width * size}px`
        }

        
         return (
                 <img onLoad={this.onImgLoad} src={src}/>
                );
     }
 }


const Image = ({ src, size }) => {
    const style = {
        // backgroundImage : `url(${src})`,
        // backgroundSize: 100% 100%,
        height: `${100 * (size / 10)}px`,
        width: `${100 * (size / 10)}px`
    }

    return (<Grid item>
        <img src={src} style={style} />
    </Grid>)
}

class LayerOutputs extends React.Component {
    render() {
        const { module, classes } = this.props

        return (
            <div >
                <Grid
                    container
                    direction="row"
                    justify="center"
                    alignItems="center"
                    spacing={8}
                >
                    <Grid item xs={12}>
                        <Typography variant="h6" gutterBottom style={{ textAlign: 'center' }}>
                            {module.state.layer.name.split('(')[0]}
                        </Typography>
                    </Grid>
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
                    {this.props.module.state.outputs.length == 0 ? 
                        (<h1>Nothing to show</h1>) : 
                        (<Button variant="contained" color="primary" onClick={() => module.getLayerOutputs()}>
                            More
                        </Button>)}
                        
                    </Grid>
                </Grid>
            </div>

        )
    }
}
export default LayerOutputs