<script lang="ts">
	import { onMount } from 'svelte';

	type CrowdLevel = {
		timestamp: string;
		branch: string;
		level: number;
	};

	let crowdLevels: CrowdLevel[] = [];
	let loading = true;
	let error: string | null = null;

	onMount(async () => {
		try {
			const res = await fetch('http://localhost:8000/crowd_levels');
			if (!res.ok) throw new Error(`Error fetching: ${res.status}`);
			crowdLevels = await res.json();
		} catch (err) {
			error = (err as Error).message;
		} finally {
			loading = false;
		}
	});
</script>

{#if loading}
	<p>Loading crowd levels...</p>
{:else if error}
	<p style="color: red;">{error}</p>
{:else}
	<ul>
		{#each crowdLevels as crowd}
			<li>
				{crowd.timestamp} — {crowd.branch}: {crowd.level}
			</li>
		{/each}
	</ul>
{/if}
