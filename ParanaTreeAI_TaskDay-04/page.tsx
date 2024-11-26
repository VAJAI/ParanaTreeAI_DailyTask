import { link } from "fs";
import Link from "next/link";

type Repository ={
  id:number;
  name:string;
  fullname:string;
}

export default async function page() {
 
  const response = await fetch ('https://api.github.com/repos/vercel/next.js');
  const data:Repository = await response.json();
  

  return (
    <>
    <h1>{data.name}</h1>
    <p><Link href='/blog/123'>Blog</Link></p>
    <p><Link href='/components'>Componet</Link></p>
    </>
  )
}
