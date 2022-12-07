import {
  AppBar,
  Box,
  LinearProgress,
  Toolbar,
  Typography,
} from "@mui/material";
import { Outlet, useNavigation } from "react-router-dom";

export function Root() {
  const navigation = useNavigation();

  return (
    <>
      <AppBar position="fixed">
        {navigation.state !== "idle" && (
          <LinearProgress
            color="inherit"
            sx={(t) => ({
              width: "100vw",
              position: "fixed",
              zIndex: t.zIndex.modal,
            })}
          />
        )}
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            App
          </Typography>
        </Toolbar>
      </AppBar>
      <Toolbar />
      <AppBar />
      <Box component="main" sx={{ py: 2 }}>
        <Outlet />
      </Box>
    </>
  );
}
