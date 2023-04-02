
# Supabase

Check `SUPABASE_TOKEN` and `SUPABASE_PROJECT_ID` in gitpod.io variable if needed

## VSCode + Deno

1. install deno extension
2. cmd+shift+p -> deno setup workspace thingy

## Functions

### Local

```bash
npx supabase start
npx supabase functions serve --no-verify-jwt --env-file ./supabase/.env.local
```

### Deploy

```bash
supabase functions deploy --no-verify-jwt stripe --project-ref $SUPABASE_PROJECT_ID --import-map supabase/functions/import_map.json 
```

