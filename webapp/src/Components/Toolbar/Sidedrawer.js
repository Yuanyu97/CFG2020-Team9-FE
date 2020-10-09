import React, { Fragment, useState } from 'react'
import MenuIcon from '@material-ui/icons/Menu'
import { makeStyles } from '@material-ui/core/styles'
import Drawer from '@material-ui/core/Drawer'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemText from '@material-ui/core/ListItemText'
import Badge from '@material-ui/core/Badge';
import NotificationsIcon from '@material-ui/icons/Notifications';
import { useHistory } from "react-router-dom";
import IconButton from '@material-ui/core/IconButton';
import AccountBoxIcon from '@material-ui/icons/AccountBox';
import VpnKeyIcon from '@material-ui/icons/VpnKey';

const useStyles = makeStyles((theme) => ({
    list: {
        width: 200,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    icon: {
        color: 'green'
    }
}))

export default function SideDrawer() {
    const classes = useStyles()
    const history = useHistory();

    const routeChange = () => {
        let path = `signin`;
        history.push(path);
    }
    const [sideDrawerIsVisible, setSideDrawerIsVisible] = useState(false)

    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return
        }
        setSideDrawerIsVisible(open)
    }

    const list = (
        <div
            className={classes.list}
            role="presentation"
            onClick={toggleDrawer(false)}
            onKeyDown={toggleDrawer(false)}
        >
            <List>
                {['Notifications', 'Profile', 'Logout'].map((text) => (
                    <ListItem button key={text} onClick={text === 'Notifications' ? () => { } : text === 'Profile' ? () => { } : routeChange}>
                        <ListItemIcon className={classes.icon} >{text === 'Notifications' ? <Badge badgeContent={4} color="error"><NotificationsIcon /></Badge> : text === 'Profile' ? <AccountBoxIcon /> : <VpnKeyIcon />}</ListItemIcon>
                        <ListItemText primary={text} />
                    </ListItem>
                ))}
            </List>
        </div>
    )

    return (
        <div>
            <Fragment>
                <IconButton style={{ marginRight: '0' }} edge="start" className={classes.menuButton} color="inherit" aria-label="menu" onClick={toggleDrawer(true)}>
                    <MenuIcon style={{ color: 'white' }} />
                </IconButton>
                <Drawer open={sideDrawerIsVisible} onClose={toggleDrawer(false)} anchor='right'>
                    {list}
                </Drawer>
            </Fragment>
        </div>
    )
}