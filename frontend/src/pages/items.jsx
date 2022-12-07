import AddIcon from "@mui/icons-material/Add";
import {
  Button,
  Card,
  CardActions,
  CardContent,
  Container,
  Fab,
  Grid,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { Form, useLoaderData } from "react-router-dom";

export function ItemIndex() {
  const items = useLoaderData();

  return (
    <Container maxWidth="sm">
      <Stack spacing={2} sx={{ mb: 8 }}>
        {items &&
          items.map(({ id, name, date }) => (
            <Card key={id}>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  {name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {new Date(date + "Z").toLocaleString()}
                </Typography>
              </CardContent>
              <CardActions>
                <Form
                  method="delete"
                  action={`${id}`}
                  onSubmit={(event) => {
                    window.confirm(
                      "Please confirm you want to delete this item."
                    ) || event.preventDefault();
                  }}
                >
                  <Button href={`${id}`}>Edit</Button>
                  <Button type="submit" color="error">
                    Delete
                  </Button>
                </Form>
              </CardActions>
            </Card>
          ))}
      </Stack>
      <Fab
        color="secondary"
        variant="extended"
        sx={(t) => ({
          position: "fixed",
          bottom: t.spacing(2),
          right: t.spacing(2),
        })}
        href="new"
      >
        <AddIcon sx={{ mr: 1 }} />
        Create New
      </Fab>
    </Container>
  );
}

export function CreateItem() {
  return <ItemForm method="post" />;
}

export function EditItem() {
  const item = useLoaderData();

  return <ItemForm method="put" defaultValues={item} />;
}

function ItemForm({ method, defaultValues }) {
  const { name } = defaultValues || {};

  return (
    <Container maxWidth="sm">
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Typography component="h1" variant="h4" align="center">
          Create Item
        </Typography>
        <Form method={method}>
          <Grid container sx={{ mt: 2 }} spacing={2} justifyContent="flex-end">
            <Grid item xs={12}>
              <TextField
                required
                type="text"
                name="name"
                label="Name"
                defaultValue={name}
                fullWidth
              />
            </Grid>
            <Grid item>
              <Button type="submit" variant="contained">
                Submit
              </Button>
            </Grid>
          </Grid>
        </Form>
      </Paper>
    </Container>
  );
}
