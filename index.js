import jsonfile from 'jsonfile'
import moment from 'moment'
import { simpleGit } from 'simple-git'
import { access, readFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const projectDirectory = dirname(fileURLToPath(import.meta.url))
const dataPath = resolve(projectDirectory, 'data.json')
const git = simpleGit(projectDirectory)
const targetRemoteUrl = 'https://github.com/ShlokMishra01/privatesm.git'
const defaultBranch = 'main'
const maxCount = 100
const managedFiles = ['.gitignore', 'README.md', 'data.json', 'index.js', 'package.json', 'package-lock.json']

// Usage:
//   node index.js
//   node index.js --message "your message"
//   node index.js --count 50
//   node index.js --count 50 --message "your message"

function normalizeRemoteUrl(url) {
  return url.trim().replace(/\/+$/, '').replace(/\.git$/i, '').toLowerCase()
}

async function fileExists(path) {
  try {
    await access(path)
    return true
  } catch (error) {
    if (error.code === 'ENOENT') return false
    throw error
  }
}

function getFlagValue(flag) {
  const index = process.argv.indexOf(flag)
  if (index === -1) return null
  const value = process.argv[index + 1]?.trim()
  if (!value || value.startsWith('--')) {
    throw new Error(`Pass a value after ${flag}.`)
  }
  return value
}

function getCommitMessage() {
  return getFlagValue('--message') ?? 'chore: update repository maintenance metadata'
}

function getCount() {
  const raw = getFlagValue('--count')
  if (raw === null) return 1
  const count = Number(raw)
  if (!Number.isInteger(count) || count < 1 || count > maxCount) {
    throw new Error(`--count must be a whole number between 1 and ${maxCount}.`)
  }
  return count
}

async function ensureRepositoryAndRemote() {
  // 'root' makes sure THIS folder is the repo, not a parent folder's repo.
  if (!(await git.checkIsRepo('root'))) {
    await git.raw(['init', '-b', defaultBranch])
  }

  const remotes = await git.getRemotes(true)
  const origin = remotes.find((remote) => remote.name === 'origin')

  if (!origin) {
    await git.addRemote('origin', targetRemoteUrl)
    return
  }

  if (normalizeRemoteUrl(origin.refs.fetch) !== normalizeRemoteUrl(targetRemoteUrl)) {
    throw new Error(
      `Refusing to push: origin points to ${origin.refs.fetch}, not ${targetRemoteUrl}.`
    )
  }
}

async function updateMaintenanceData() {
  const exists = await fileExists(dataPath)
  const data = exists ? await jsonfile.readFile(dataPath) : {}

  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    throw new Error('data.json must contain a JSON object.')
  }

  const maintenance = data.maintenance ?? {}
  if (!maintenance || typeof maintenance !== 'object' || Array.isArray(maintenance)) {
    throw new Error('The maintenance property in data.json must be a JSON object.')
  }

  const now = moment().toISOString()
  data.project = data.project ?? 'privatesm'
  data.maintenance = {
    ...maintenance,
    updatedAt: now,
    lastRunAt: now,
    runCount: (Number.isInteger(maintenance.runCount) && maintenance.runCount >= 0
      ? maintenance.runCount
      : 0) + 1
  }

  await jsonfile.writeFile(dataPath, data, { spaces: 2 })
}

async function commitOnce(message) {
  await updateMaintenanceData()

  const status = await git.status()
  const changedManagedFiles = status.files
    .filter((file) => managedFiles.includes(file.path))
    .map((file) => file.path)

  if (changedManagedFiles.length === 0) return false

  await git.add(changedManagedFiles)
  await git.commit(message, changedManagedFiles)
  return true
}

async function main() {
  const count = getCount()
  const baseMessage = getCommitMessage()

  await ensureRepositoryAndRemote()

  const initialStatus = await git.status()
  const stagedOutsideProject = initialStatus.files
    .filter((file) => file.index !== ' ' && file.index !== '?' && !managedFiles.includes(file.path))
    .map((file) => file.path)
  if (stagedOutsideProject.length > 0) {
    throw new Error(
      `Refusing to include pre-staged files outside the automation project: ${stagedOutsideProject.join(', ')}`
    )
  }

  let made = 0
  for (let i = 1; i <= count; i++) {
    const message = count > 1 ? `${baseMessage} (${i}/${count})` : baseMessage
    if (await commitOnce(message)) {
      made++
      console.log(`Commit ${i}/${count} created.`)
    }
  }

  if (made === 0) {
    console.log('No changes to commit.')
    return
  }

  const branch = (await git.status()).current
  if (!branch) {
    throw new Error('Cannot push from a detached HEAD; check out a branch first.')
  }

  await git.push('origin', branch, ['--set-upstream'])
  console.log(`Created and pushed ${made} commit(s) to origin/${branch}.`)
}

main().catch((error) => {
  console.error('Git maintenance workflow failed:', error)
  process.exitCode = 1
})