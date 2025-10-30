'use client';
import { useEffect, useState } from 'react';

const API_BASE = 'http://localhost:4000';
const ADMIN_USER_ID = ''; // Set after running seed script

export default function AdminMockClient() {
  const [products, setProducts] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [adminId, setAdminId] = useState(ADMIN_USER_ID);

  const fetchProducts = async () => {
    if (!adminId) return;
    try {
      const res = await fetch(`${API_BASE}/admin/products`, {
        headers: { 'x-user-id': adminId }
      });
      if (res.ok) {
        const data = await res.json();
        setProducts(data.items || []);
      } else {
        alert('Failed to fetch products. Check admin ID.');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/stats/top`);
      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (adminId) {
      fetchProducts();
    }
    fetchStats();
  }, [adminId]);

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Admin Platform - Client Mock</h1>
      <p style={{ marginBottom: '1rem', color: '#666' }}>
        Enter admin user ID (from seed script output) to test RBAC.
      </p>
      
      <input 
        placeholder="Admin User ID"
        value={adminId}
        onChange={e => setAdminId(e.target.value)}
        style={{ padding: '0.5rem', marginBottom: '2rem', width: '300px' }}
      />

      <h2>Top Products by Revenue (Cached)</h2>
      {stats && (
        <div style={{ marginBottom: '2rem' }}>
          <p style={{ fontSize: '0.875rem', color: '#666' }}>
            Cached: {stats.cached ? 'Yes' : 'No'}
          </p>
          {stats.items.map((item: any, i: number) => (
            <div key={i} style={{ padding: '0.5rem', borderBottom: '1px solid #eee' }}>
              <strong>{item.productName}</strong> - 
              Revenue: ${(item.totalRevenue / 100).toFixed(2)} - 
              Orders: {item.orderCount}
            </div>
          ))}
        </div>
      )}

      <h2>Admin: Products</h2>
      {products.length === 0 && <p>No products or not authorized</p>}
      {products.map(p => (
        <div key={p.id} style={{ padding: '0.5rem', borderBottom: '1px solid #eee' }}>
          {p.name} - ${(p.priceCents / 100).toFixed(2)} - Stock: {p.stock}
        </div>
      ))}
    </div>
  );
}

