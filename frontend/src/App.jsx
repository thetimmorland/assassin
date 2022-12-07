import { ThemeProvider } from "@emotion/react";
import { CssBaseline } from "@mui/material";
import {
  createBrowserRouter,
  redirect,
  RouterProvider,
} from "react-router-dom";
import { DefaultService, OpenAPI } from "./client";
import { CreateItem, EditItem, ItemIndex } from "./pages/items";
import { Root } from "./pages/root";
import { theme } from "./theme";

export default function App() {
  OpenAPI.BASE = "http://127.0.0.1:8000";

  const router = createBrowserRouter([
    {
      path: "/",
      element: <Root />,
      children: [
        {
          path: "/",
          element: <ItemIndex />,
          loader: async () => {
            return await DefaultService.getItems();
          },
        },
        {
          path: "/new",
          element: <CreateItem />,
          action: async ({ request }) => {
            const formData = await request.formData();
            const item = Object.fromEntries(formData);
            await DefaultService.createItem(item);
            return redirect("/");
          },
        },
        {
          path: "/:id",
          element: <EditItem />,
          loader: async ({ params }) => {
            return await DefaultService.getItem(params.id);
          },
          action: async ({ request, params }) => {
            switch (request.method) {
              case "PUT":
                const formData = await request.formData();
                const item = Object.fromEntries(formData);
                await DefaultService.updateItem(params.id, item);
                return redirect("/");
              case "DELETE":
                await DefaultService.deleteItem(params.id);
                return redirect("/");
              default:
                throw new Error(`Unexpected request method: ${request.method}`);
            }
          },
        },
      ],
    },
  ]);

  return (
    <>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </>
  );
}
