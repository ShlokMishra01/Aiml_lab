import jsonfile from 'jsonfile'
import moment from 'moment'
import { simpleGit } from 'simple-git'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const projectDirectory = dirname(fileURLToPath(import.meta.url))
const dataPath = resolve(projectDirectory, 'data.json')
const targetRemoteUrl = 'https://github.com/ShlokMishra01/privatesm.git'
const maxTotal = 1500

const git = simpleGit(projectDirectory)

function normalizeRemoteUrl(url) {
  return url.trim().replace(/\/+$/, '').replace(/\.git$/i, '').toLowerCase()
}

function getFlag(flag, fallback) {
  const index = process.argv.indexOf(flag)
  if (index === -1) return fallback
  const value = process.argv[index + 1]?.trim()
  if (!value || value.startsWith('--')) throw new Error(`Pass a value after ${flag}.`)
  return value
}

function getInt(flag, fallback) {
  const n = Number(getFlag(flag, String(fallback)))
  if (!Number.isInteger(n) || n < 1) throw new Error(`${flag} must be a whole number of 1 or more.`)
  return n
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = randInt(0, i)
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return arr
}

async function checkRemote() {
  if (!(await git.checkIsRepo('root'))) {
    throw new Error('This folder is not the root of a git repo. Run inside the privatesm folder.')
  }
  const remotes = await git.getRemotes(true)
  const origin = remotes.find((r) => r.name === 'origin')
  if (!origin) throw new Error('No origin remote found.')
  if (normalizeRemoteUrl(origin.refs.fetch) !== normalizeRemoteUrl(targetRemoteUrl)) {
    throw new Error(`Refusing to push: origin is ${origin.refs.fetch}, not ${targetRemoteUrl}.`)
  }
}

// Usage:
//   node backdate.js
//   node backdate.js --from 2026-01-01 --to 2026-07-31 --daysMin 3 --daysMax 5 --min 15 --max 20
function buildDates() {
  const from = moment(getFlag('--from', '2026-01-01'), 'YYYY-MM-DD', true)
  const to = moment(getFlag('--to', '2026-07-31'), 'YYYY-MM-DD', true)
  if (!from.isValid() || !to.isValid() || to.isBefore(from)) {
    throw new Error('Use valid dates as YYYY-MM-DD, with --to after --from.')
  }
  if (to.isAfter(moment())) throw new Error('--to cannot be in the future.')

  const daysMin = getInt('--daysMin', 3)
  const daysMax = getInt('--daysMax', 5)
  const perDayMin = getInt('--min', 15)
  const perDayMax = getInt('--max', 20)
  if (daysMax < daysMin || perDayMax < perDayMin) {
    throw new Error('Max values must be greater than or equal to min values.')
  }

  const dates = []
  const cursor = from.clone().startOf('month')

  while (cursor.isSameOrBefore(to)) {
    const monthStart = moment.max(cursor.clone(), from).startOf('day')
    const monthEnd = moment.min(cursor.clone().endOf('month'), to).startOf('day')
    const available = []
    for (const d = monthStart.clone(); d.isSameOrBefore(monthEnd); d.add(1, 'day')) {
      available.push(d.clone())
    }

    const howManyDays = Math.min(randInt(daysMin, daysMax), available.length)
    const chosenDays = shuffle(available).slice(0, howManyDays)

    for (const day of chosenDays) {
      const commitsToday = randInt(perDayMin, perDayMax)
      for (let k = 0; k < commitsToday; k++) {
        dates.push(day.clone().hour(randInt(8, 22)).minute(randInt(0, 59)).second(randInt(0, 59)))
      }
    }
    cursor.add(1, 'month')
  }

  dates.sort((a, b) => a.valueOf() - b.valueOf())
  if (dates.length > maxTotal) throw new Error(`Too many commits (${dates.length}). Lower the settings.`)
  return dates
}

async function main() {
  const dates = buildDates()
  await checkRemote()

  const total = dates.length
  console.log(`Planning ${total} commits...`)

  for (let i = 0; i < total; i++) {
    const date = dates[i].format()
    await jsonfile.writeFile(dataPath, { date, commit: i + 1 }, { spaces: 2 })

    await git.add(['data.json'])
    await git.commit(`chore: update data (${dates[i].format('YYYY-MM-DD')})`, ['data.json'], {
      '--date': date
    })
    console.log(`Commit ${i + 1}/${total} -> ${date}`)
  }

  const branch = (await git.status()).current
  if (!branch) throw new Error('Detached HEAD; check out a branch first.')
  await git.push('origin', branch)
  console.log(`Done. Pushed ${total} commits to origin/${branch}.`)
}

main().catch((error) => {
  console.error('Backdate script failed:', error)
  process.exitCode = 1
})