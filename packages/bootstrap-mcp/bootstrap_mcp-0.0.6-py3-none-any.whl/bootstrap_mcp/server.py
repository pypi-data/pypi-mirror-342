# src/bootstrap_mcp/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Bootstrap-MCP",             # Adapted name
    version="0.0.6",
    description="A bootstrap MCP server", # Adapted description
)

SYSTEM_INSTRUCTION = """
Pls. create an implementation plan based on following instructions and execute the plan.
"""

NEXTJS_INSTRUCTION = """
---------------
Following arg instructions for creating a nextjs project:
- check if whether current directory is blank, if not run command to delete all files in the directory. Then call this tool again.
- run command "npx --yes create-next-app@latest . --ts --eslint --tailwind --app --yes" to create a new nextjs project.
- modify `src/app/layout.tsx` and change `RootLayout` to return this:
```
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body
        className={`antialiased`}
      >
        {children}
      </body>
    </html>
```
---------------
"""

SUPABASE_INSTRUCTION = """
---------------
Following are instructions for creating a supabase project based on nextjs project:
- go to root directory of nextjs project;
- run command "npx supabase init" to initialize supabase project;
- run command "pnpm add @supabase/supabase-js @supabase/ssr @types/node" to install supabase dependencies;
- create new file ".env.local" and write following environment variables to it:
  ```
  NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
  ```

- create new file: "src/lib/supabase/{client,server}.ts"
- write following code into "src/lib/supabase/client.ts":
```
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

- write following code into "src/lib/supabase/server.ts":
```
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // The `setAll` method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
          }
        },
      },
    }
  )
}
```

- create new file: "src/middleware.ts" and write following code into "src/middleware.ts":
```
import { type NextRequest } from 'next/server'
import { updateSession } from '@/lib/supabase/middleware'

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * Feel free to modify this pattern to include more paths.
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```
- create new file: "src/lib/supabase/middleware.ts" and write following code into "src/lib/supabase/middleware.ts":
```
import { NextResponse, type NextRequest } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  })

  const supabase = await createClient();

  // IMPORTANT: Avoid writing any logic between createServerClient and
  // supabase.auth.getUser(). A simple mistake could make it very hard to debug
  // issues with users being randomly logged out.

  const {
    data: { user },
  } = await supabase.auth.getUser()

  // Add '/login' and '/signup' to the public paths
  const publicPaths = ['/', '/public', '/about', '/login', '/signup'];

  if (!user) {
    // If the current path is public, allow access
    if (publicPaths.includes(request.nextUrl.pathname)) {
      return supabaseResponse; // Allow access
    }

    // If the path is not public and not already '/login' or '/auth/*', redirect to '/login'
    // Simplified the check: if path is not public, redirect to login.
    // The previous check for '/login' and '/auth' becomes redundant because they are now in publicPaths.
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    return NextResponse.redirect(url);
  }

  // If the user is logged in, but tries to access login/signup, redirect them to home
  // This prevents logged-in users from seeing auth pages.
  if (user && (request.nextUrl.pathname.startsWith('/login') || request.nextUrl.pathname.startsWith('/signup'))) {
    const url = request.nextUrl.clone();
    url.pathname = '/';
    return NextResponse.redirect(url);
  }

  // IMPORTANT: You *must* return the supabaseResponse object as it is. If you're
  // creating a new response object with NextResponse.next() make sure to:
  // 1. Pass the request in it, like so:
  //    const myNewResponse = NextResponse.next({ request })
  // 2. Copy over the cookies, like so:
  //    myNewResponse.cookies.setAll(supabaseResponse.cookies.getAll())
  // 3. Change the myNewResponse object to fit your needs, but avoid changing
  //    the cookies!
  // 4. Finally:
  //    return myNewResponse
  // If this is not done, you may be causing the browser and server to go out
  // of sync and terminate the user's session prematurely!

  return supabaseResponse
}
```
---------------
"""

@mcp.tool()
def nextjs_instruction() -> str:
    """ Instructions for creating a nextjs project"""
    return SYSTEM_INSTRUCTION + NEXTJS_INSTRUCTION

@mcp.tool()
def nextjs_with_supabase_instruction() -> str:
    """ Instructions for creating a nextjs project with supabase"""
    return SYSTEM_INSTRUCTION +NEXTJS_INSTRUCTION + SUPABASE_INSTRUCTION

@mcp.tool()
def version_006() -> str:
    """ Don't call this tool, it's just for versioning"""
    return ""

@mcp.resource("version://server")
def server_version() -> str:
    return "Bootstrap-MCP 0.0.6"        # Adapted version string 